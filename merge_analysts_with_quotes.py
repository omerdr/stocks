'''
Input format: (no header line)
Ticker,Date,Firm,Action,Rating,Price Target
Sample input: AAL,6/11/2015,JPMorgan Chase & Co.,Reiterated Rating,Overweight,

hisotrical quote directory:
needs to contain a txt file for every ticker in the format (with header line!):
Date,Open,High,Low,Close,Volume,Adj Close
Sample GOOG.txt: 2015-06-29,525.01001,528.609985,520.539978,521.52002,1930900,521.52002

Run with:
cat data/marketbeat_nasdaq.csv | python price_change_hist.py > data/marketbeat_nasdaq_price_changes_TIMEDIFF.csv

Also (for separating analysts):
cd ~/github/stocks/data/top20_analysts
find . | parallel "cat {} | python ../../price_change_hist.py --pickle-file {}.pkl -"

pycharm args:
--pickle-file data/top20_analysts/test-bank-of-america.pkl "data/top20_analysts/Bank of America.csv"
data/marketbeat_nasdaq.csv

'''
from collections import defaultdict

import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from myutils import save_obj, find_closest, DatesNotAvailableException
from ordereddefaultdict import OrderedDefaultdict
import re
import click

FIELD_REC_TICKER    = 0
FIELD_REC_DATE      = 1
FIELD_REC_FIRM      = 2
FIELD_REC_RANK      = 4
FIELD_REC_PRICE_1Y  = 5

FIELD_QUOTE_DATE    = 0
FIELD_QUOTE_PRICE   = 4 # take the close price

RECS_DATE_FORMAT = '%m/%d/%Y'
QUOTES_DATE_FORMAT = '%Y-%m-%d'
HISTORICAL_QUOTES_PATH = '/home/omer/code/github/stocks/historical-quotes/'
#DEFAULT_RANKING_PICKLE_FILE = 'data/ranking.pkl'
DATE_CHANGE = relativedelta(years=1)  # months=6)

HEADER_LINE = 'Ticker,Firm,Action,Date,Old Target,New Target,Target Ratio,Current Price,Price in a year,Price Ratio'

def get_price_change(ticker, start_date, end_date):
    with open(HISTORICAL_QUOTES_PATH + ticker.upper() + '.txt', 'r') as fp:
        # build quotes list for the selected stock
        quotes = OrderedDefaultdict(list)
        cp = csv.reader(fp)

        try:
            cp.next()  # skip header line
        except StopIteration:
            raise DatesNotAvailableException

        for l in cp:
            if len(l) < FIELD_QUOTE_PRICE:
                continue
            quotes[datetime.strptime(l[FIELD_QUOTE_DATE], QUOTES_DATE_FORMAT)] = float(l[FIELD_QUOTE_PRICE])

        if not quotes or start_date < quotes.keys()[-1] or end_date > quotes.keys()[0]:
            raise DatesNotAvailableException

        start = quotes[find_closest(quotes.keys(), start_date)]
        end = quotes[find_closest(quotes.keys(), end_date)]

        return start, end, end / start


@click.command()
@click.option('--pickle-file', help='ranking dictionary pickle output file', default=None, type=unicode)  # default=DEFAULT_RANKING_PICKLE_FILE,
@click.argument('input', type=click.File('rb'))
def price_change_hist(input, pickle_file):
    ranking = defaultdict(list)
    print HEADER_LINE
    for l in csv.reader(input):
        rec_date = datetime.strptime(l[FIELD_REC_DATE], RECS_DATE_FORMAT)
        later_date = rec_date + DATE_CHANGE

        try:
            start, end, delta = get_price_change(l[FIELD_REC_TICKER], rec_date, later_date)
        except DatesNotAvailableException:  # Catch when dates are not available
            continue

        to_rank = re.sub('(.*\s*->\s*)(?P<to>.*)', '\\g<to>', l[FIELD_REC_RANK])
        if delta:
            ranking[to_rank].append(delta)

        # get rid of annoying commas in text
        for i in range(len(l)):
            l[i] = l[i].replace(",",";")

        # Don't deal with exchange rates
        l[FIELD_REC_PRICE_1Y] = l[FIELD_REC_PRICE_1Y].replace('$','')

        # Make sure this isn't a different currency (&euro; or C$ or something else)
        if any(c.isalpha() for c in l[FIELD_REC_PRICE_1Y]):
            continue

        # replace '$40.00 -> $42.00' to '40.00,42.00'
        before_after = l[FIELD_REC_PRICE_1Y].split('->')
        if len(before_after) == 1:
            l[FIELD_REC_PRICE_1Y] = before_after[0] + ',' + before_after[0] + ',1.0'   # before and after are equal
        elif len(before_after) == 2:
            l[FIELD_REC_PRICE_1Y] = ','.join(before_after).replace(' ','') + \
                                    ',' + str(float(before_after[1])/float(before_after[0]))
        else:
            raise ValueError

        print ",".join([l[FIELD_REC_TICKER], l[FIELD_REC_FIRM], to_rank, l[FIELD_REC_DATE],
                        l[FIELD_REC_PRICE_1Y],  # before, after, ratio
                        str(start), str(end), str(delta)])

    if pickle_file:
        save_obj(ranking, pickle_file)


if __name__ == "__main__":
    try:
        price_change_hist()
        # with open('data/marketbeat_nasdaq.csv') as fp:
        #     price_change_hist(fp)
    except KeyboardInterrupt:
        pass