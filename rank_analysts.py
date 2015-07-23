"""
Input file format (with header):
Ticker,Firm,Action,Date,Old Target,New Target,Target Ratio,Current Price,Price in a year,Price Ratio
AAL,Goldman Sachs,Buy,6/10/2014,43.59,50.00,1.14705207616,43.264049,40.43,0.934494133917
AAL,Stifel Nicolaus,Buy,5/5/2014,45.00,45.00,1.0,36.268074,47.009998,1.296181264
AAL,JPMorgan Chase & Co.,Overweight,5/1/2014,55.00,55.00,1.0,36.05998,49.389999,1.36966240691
AAL,Bank of America,Neutral,4/28/2014,40.00,42.00,1.05,34.841135,51.085274,1.46623449552
"""
from datetime import datetime
import os
import click
import csv
import errno
from financial_utils import PRICE_CHANGE_FIELDS, FindPrice, PRICE_CHANGE_DATE_FORMAT
from myutils import DatesNotAvailableException, ZeroBasedEnum

HEADER_LINE = 'Ticker,Firm,Action,Date,CurrentPrice,TargetPrice,EOQ_FinalPrice,L1PercentageDistance'

@click.command()
@click.option('--header/--no-header', default=False)
@click.option('--find-quotes/--use-input-quotes', default=True, help='Set --use-input-quotes to use input file for '
                                                                     '"current price" and "price in a year".')
@click.option('--quotes-dir', default=os.getcwd(),
              help='The path containing a txt file for every company with it\'s historical prices. Only needed when '
                   '--use-input-quotes isn\'t set')
@click.argument('reco_file', type=click.File('rb'))  # , help='analyst recommendations file')
def rank_analysts(header, find_quotes, quotes_dir, reco_file):
    find_price = FindPrice(quotes_dir)

    f_reco = csv.reader(reco_file)
    if header:
        f_reco.next()

    print HEADER_LINE
    for l in f_reco:

        if (l[PRICE_CHANGE_FIELDS.Firm.zvalue] and
            l[PRICE_CHANGE_FIELDS.Date.zvalue] and
            l[PRICE_CHANGE_FIELDS.Ticker.zvalue] and
            l[PRICE_CHANGE_FIELDS.New_Target.zvalue] and
            l[PRICE_CHANGE_FIELDS.Current_Price.zvalue]):

            current_date = datetime.strptime(l[PRICE_CHANGE_FIELDS.Date.zvalue], PRICE_CHANGE_DATE_FORMAT)
            target_price = float(l[PRICE_CHANGE_FIELDS.New_Target.zvalue])

            if not find_quotes:
                current_price = float(l[PRICE_CHANGE_FIELDS.Current_Price.zvalue])
                final_price = float(l[PRICE_CHANGE_FIELDS.Price_in_a_year.zvalue])

            else:
                try:
                    # find quotes instead of trusting the input file
                    current_price = find_price.at(l[PRICE_CHANGE_FIELDS.Ticker.zvalue], current_date)
                    final_price = find_price.at_end_of_qtr_next_year(l[PRICE_CHANGE_FIELDS.Ticker.zvalue], current_date)
                except DatesNotAvailableException:
                    continue

            to_print = [l[PRICE_CHANGE_FIELDS.Ticker.zvalue], l[PRICE_CHANGE_FIELDS.Firm.zvalue],
                        l[PRICE_CHANGE_FIELDS.Action.zvalue],
                        current_date.date(), current_price, target_price,
                        final_price, abs(final_price - target_price) / current_price]

            print ",".join([str(i) for i in to_print])

if __name__ == "__main__":
    try:
        rank_analysts()
    except KeyboardInterrupt:
        pass
    except IOError, e:
        if e.errno != errno.EPIPE:
            raise e
