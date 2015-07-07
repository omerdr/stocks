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
'''
from collections import defaultdict

import csv
#from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bisect import bisect_left
from sys import stdin
from ordereddefaultdict import OrderedDefaultdict, DefaultOrderedDict
import pickle
import re
import click

FIELD_REC_TICKER    = 0
FIELD_REC_DATE      = 1
FIELD_REC_FIRM      = 2
FIELD_REC_RANK      = 4
FIELD_REC_PRICE_1Y  = 5

FIELD_QUOTE_DATE    = 0
FIELD_QUOTE_PRICE   = 6 # take the adjusted closing price

RECS_DATE_FORMAT = '%m/%d/%Y'
QUOTES_DATE_FORMAT = '%Y-%m-%d'
HISTORICAL_QUOTES_PATH = '/home/omer/code/github/stocks/historical-quotes/'
#DEFAULT_RANKING_PICKLE_FILE = 'data/ranking.pkl'
DATE_CHANGE = relativedelta(years=1)  # months=6)

def find_closest(myList, myNumber):
    """
    (Doesn't Assume myList is sorted.) Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    sorted_list = sorted(myList)
    pos = bisect_left(sorted_list, myNumber)
    if pos == 0:
        return sorted_list[0]
    if pos == len(sorted_list):
        return sorted_list[-1]
    before = sorted_list[pos - 1]
    after = sorted_list[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before

class DatesNotAvailableException(Exception):
    pass

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

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
    for l in csv.reader(input):
        rec_date = datetime.strptime(l[FIELD_REC_DATE], RECS_DATE_FORMAT)
        later_date = rec_date + DATE_CHANGE

        try:
            start, end, delta = get_price_change(l[FIELD_REC_TICKER], rec_date, later_date)
        except DatesNotAvailableException:  # Catch when dates are not available
            continue

        if delta:
            ranking[re.sub('(.*\s*->\s*)(?P<to>.*)', '\\g<to>', l[FIELD_REC_RANK])].append(delta)

        # get rid of annoying commas in text
        for t in l:
            t = t.replace(",", ";")

        print ",".join([l[FIELD_REC_TICKER], l[FIELD_REC_FIRM],
                        re.sub('(.*\s*->\s*)(?P<to>.*)', '\\g<to>', l[FIELD_REC_RANK]),
                        l[FIELD_REC_DATE], l[FIELD_REC_PRICE_1Y], str(start), str(end), str(delta)])

    if pickle_file:
        save_obj(ranking, pickle_file)


if __name__ == "__main__":
    try:
        price_change_hist()
        # with open('data/marketbeat_nasdaq.csv') as fp:
        #     price_change_hist(fp)
    except KeyboardInterrupt:
        pass