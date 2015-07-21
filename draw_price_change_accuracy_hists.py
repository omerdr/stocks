'''
input file structure (with header line):
HEADER_LINE = 'Ticker,Firm,Action,Date,Old Target,New Target,Target Ratio,Current Price,Price in a year,Price Ratio'
'''

from math import ceil

from matplotlib import pyplot as plt
import click
from collections import defaultdict
import csv
from myutils import ZeroBasedEnum, draw_hist

HEADER_LINE = 'Ticker,Firm,Action,Date,Old_Target,New_Target,Target_Ratio,Current_Price,Price_in_a_year,Price_Ratio'
FIELDS = ZeroBasedEnum('FIELDS', HEADER_LINE)

def analyst_accuracies(price_change_file):
    fp = csv.reader(price_change_file)
    fp.next()
    for l in fp:
        if (l[FIELDS.Firm.zvalue] and
            l[FIELDS.Price_in_a_year.zvalue] and
            l[FIELDS.New_Target.zvalue] and
            l[FIELDS.Current_Price.zvalue]):

            yield (l[FIELDS.Firm.zvalue],
                   abs(float(l[FIELDS.Price_in_a_year.zvalue]) -
                       float(l[FIELDS.New_Target.zvalue])) /
                   float(l[FIELDS.Current_Price.zvalue]))

@click.command()
@click.argument('input', type=click.File('rb'))
def draw_distributions(input):
    accuracies = []
    per_firm_accuracy = defaultdict(list)
    for firm, accuracy in analyst_accuracies(input):
        accuracies.append(accuracy)
        per_firm_accuracy[firm].append(accuracy)

    p = plt.figure()
    p.canvas.set_window_title("All Analysts")
    draw_hist("All Analysts",accuracies, range=(0,2.0))

    p = plt.figure()
    plots = sum([len(v) > 200 for v in per_firm_accuracy.itervalues()])
    i = 1
    for firm,values in per_firm_accuracy.iteritems():
        if len(values) > 200:
            plt.subplot(4, ceil(plots / 4.0), i)
            draw_hist(firm, values, range=(0,2.0))
            i += 1

    plt.suptitle('Count vs. Accuracy (|New Price - Target| / |Original Price|)')
    p.canvas.set_window_title("Each Analyst Separately")
    plt.show()

if __name__ == "__main__":
    try:
        draw_distributions()
    except KeyboardInterrupt:
        pass