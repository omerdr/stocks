"""
Input format: (no header line)
Ticker,Date,Firm,Action,Rating,Price Target
Sample input: AAL,6/11/2015,JPMorgan Chase & Co.,Reiterated Rating,Overweight,

hisotrical quote directory:
needs to contain a txt file for every ticker in the format (with header line!):
Date,Open,High,Low,Close,Volume,Adj Close
Sample GOOG.txt: 2015-06-29,525.01001,528.609985,520.539978,521.52002,1930900,521.52002

Run with:
python merge_analysts_with_quotes.py --historical-quotes-dir=historical-quotes data/marketbeat_nasdaq.csv

Also (for separating analysts):
cd ~/github/stocks/data/top20_analysts
find . | parallel "cat {} | python ../../merge_analysts_with_quotes.py --pickle-file {}.pkl -"
"""
from collections import defaultdict

import csv
from datetime import datetime
import errno
from myutils import save_obj, DatesNotAvailableException
import re
import click

from financial_utils import FindPrice, ANALYST_DATA_FIELDS, ANALYST_DATA_DATE_FORMAT

@click.command()
@click.option('--pickle-file', help='ranking dictionary pickle output file', default=None)
@click.option('--historical-quotes-dir', help='folder containing historical quotes files', default=None)
@click.option('--header/--no-header', default=False, help='use when input file contains a header line. Default False.')
@click.option('--header-for-quotes/--no-header-for-quotes', help='quote files have header. Default True.', default=True)
@click.option('--use-current-date/--use-start-of-qtr', default=False, help='set --use-current-date to use the quote '
              'on the day that the recommendation was given, instead of the default start of quarter quote')
@click.argument('input', type=click.File('rb'))
def price_change_hist(input, pickle_file, historical_quotes_dir, header, header_for_quotes, use_current_date):
    ranking = defaultdict(list)
    find_quotes = FindPrice(historical_quotes_dir, header_for_quotes)

    if header:
        input.next()

    if use_current_date:
        HEADER_LINE = 'Ticker,Firm,Action,Date,Old_Target,New_Target,Target_Ratio,Current_Price,Price_in_1yr,Price_Ratio'
    else:
        HEADER_LINE = 'Ticker,Firm,Action,Date,Old_Target,New_Target,Target_Ratio,SOQ_Price,Price_EOQ_next_year,Price_Ratio'

    print HEADER_LINE

    for l in csv.reader(input):
        rec_date = datetime.strptime(l[ANALYST_DATA_FIELDS.Date.zvalue], ANALYST_DATA_DATE_FORMAT)

        try:
            if use_current_date:
                start_price = find_quotes.at(l[ANALYST_DATA_FIELDS.Ticker.zvalue], rec_date)
            else:
                start_price = find_quotes.at_start_of_qtr(l[ANALYST_DATA_FIELDS.Ticker.zvalue], rec_date)
            end_price = find_quotes.at_end_of_qtr_next_year(l[ANALYST_DATA_FIELDS.Ticker.zvalue], rec_date)
            price_delta = end_price / start_price
        except DatesNotAvailableException:  # Catch when dates are not available
            continue

        to_rating = re.sub('(.*\s*->\s*)(?P<to>.*)', '\\g<to>', l[ANALYST_DATA_FIELDS.Rating.zvalue])
        if pickle_file and price_delta:
            ranking[to_rating].append(price_delta)

        # get rid of annoying commas in text
        for i in range(len(l)):
            l[i] = l[i].replace(",",";")

        # Don't deal with exchange rates
        l[ANALYST_DATA_FIELDS.Price_Target.zvalue] = l[ANALYST_DATA_FIELDS.Price_Target.zvalue].replace('$','')

        # Make sure this isn't a different currency (&euro; or C$ or something else)
        if any(c.isalpha() for c in l[ANALYST_DATA_FIELDS.Price_Target.zvalue]):
            continue

        # replace '$40.00 -> $42.00' to '40.00,42.00'
        before_after = l[ANALYST_DATA_FIELDS.Price_Target.zvalue].split('->')
        if len(before_after) == 1:
            l[ANALYST_DATA_FIELDS.Price_Target.zvalue] = before_after[0] + ',' + before_after[0] + ',1.0'
        elif len(before_after) == 2:
            l[ANALYST_DATA_FIELDS.Price_Target.zvalue] = ','.join(before_after).replace(' ','') + \
                                    ',' + str(float(before_after[1])/float(before_after[0]))
        else:
            raise ValueError

        print ",".join([l[ANALYST_DATA_FIELDS.Ticker.zvalue], l[ANALYST_DATA_FIELDS.Firm.zvalue], to_rating,
                        l[ANALYST_DATA_FIELDS.Date.zvalue], l[ANALYST_DATA_FIELDS.Price_Target.zvalue],
                        str(start_price), str(end_price), str(price_delta)])

    if pickle_file:
        save_obj(ranking, pickle_file)


if __name__ == "__main__":
    try:
        price_change_hist()
    except KeyboardInterrupt:
        pass
    except IOError, e:
        if e.errno != errno.EPIPE:
            raise e
