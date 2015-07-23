import csv
import click
import errno
from myutils import ZeroBasedEnum

IN_HEADER_LINE = 'Ticker,Firm,Action,Date,SOQ_Price,TargetPrice,EOQ_FinalPrice,r_i,Count_Ticker,Normalized_r_i,r_i_bar,Avg_TargetPrice'
OUT_HEADER_LINE = "Ticker,Firm,Date,SOQPrice,EOQFinalPrice,TargetPrice,r_i-bar,r_i,r_c-bar,r_i/r_c-bar"

# TODO: Problem: When averaging with 'normalize_field' you average across every item with the same ticker, that means
# TODO: That different quarters are calculated together. Solution: Use data from one quarter instead of the entire year.
# TODO: Do this with awk, on the data before normalizing (so that r_i will actually be correct).

@click.command()
@click.option('--header/--no-header', default=False)
@click.argument('input_file', type=click.File('rb'))  # , help='analyst recommendations file')
def calc_normalized_accuracy(input_file, header):
    """
    Calculates r_c-bar and the ratio (r_i / r_c-bar)
    Run with:
    cat data/marketbeat_nasdaq_L1_SOQ_EOQ.csv | python normalize_field.py --header --value-field-number=7 - | \
    python normalize_field.py --header --value-field-number=5 --average - | \
    python calc_normalized_accuracy.py --header - | less

    Preliminaries:
    python merge_analysts_with_quotes.py --historical-quotes-dir=historical-quotes data/marketbeat_nasdaq.csv | pv > data/marketbeat_baseline_SOQ_EOQ_price_target_change.csv
    python rank_analysts.py --header --quotes-dir=historical-quotes  data/marketbeat_baseline_SOQ_EOQ_price_target_change.csv | pv > data/marketbeat_nasdaq_L1_SOQ_EOQ.csv

    Input:
    Ticker,Firm,Action,Date,SOQ_Price,TargetPrice,EOQ_FinalPrice,L1PercentageDistance,Normalized_L1PercentageDistance,Avg_TargetPrice
    """
    cp = csv.reader(input_file)

    if header:
        cp.next()

    F = ZeroBasedEnum("F",IN_HEADER_LINE)
    print OUT_HEADER_LINE
    for l in cp:
        r_i = float(l[F.r_i.zvalue])
        # r_i_bar = float(l[F.r_i_bar.zvalue])
        r_c_bar = abs(float(l[F.Avg_TargetPrice.zvalue]) - float(l[F.EOQ_FinalPrice.zvalue])) / float(l[F.SOQ_Price.zvalue])

        relative_accuracy = r_i / r_c_bar if r_c_bar else ''

        data = [l[F.Ticker.zvalue], l[F.Firm.zvalue], l[F.Date.zvalue],
                l[F.SOQ_Price.zvalue], l[F.EOQ_FinalPrice.zvalue],
                l[F.TargetPrice.zvalue], l[F.r_i_bar.zvalue],
                # r_i_bar, r_c_bar, r_i_bar / r_c_bar]
                r_i, r_c_bar, relative_accuracy]

        print ",".join([str(d) for d in data])

if __name__ == "__main__":
    try:
        calc_normalized_accuracy()
    except KeyboardInterrupt:
        pass
    except IOError, e:
        if e.errno != errno.EPIPE:
            raise e
