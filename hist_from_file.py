import csv
from numpy import mean, std, median
import click
from math import ceil
from myutils import draw_hist
from collections import defaultdict
from matplotlib import pyplot as plt

@click.command()
@click.option('--header/--no-header', default=False, help='use when input file contains a header line. Default False.')
@click.option('--threshold', default=20, help='Don\'t draw histograms for less than [threshold] values. Default 20.')
@click.option('--range-max', default=None, help='The maximum value of the x-axis in the histogram')
@click.option('--range-min', default=None, help='The minimum value of the x-axis in the histogram')
@click.option('--stats/--no-stats', default=True, help='Add stats to titles')
@click.option('--markers/--no-markers', default=False, help='Add vertical markers to plot')
@click.option('--columns', default=4, help='Number of columns in the figure (number of subplots in every row)')
@click.option('--vert-space', default=0.5, help='Vertical spacing between subplots. Default 0.5.')
@click.argument('input_file', type=click.File('r'))
def hist_from_file(input_file, header, threshold, range_min, range_max, stats, markers, columns, vert_space):
    """ Gets comma separated key-value pairs, and plots hist of the values for every key
    (given more than threshold occurrences) """
    values = defaultdict(list)
    fp = csv.reader(input_file)

    h = [None, "Values"]  # Init h so that h[1] will hold the xlabel header or no header
    if header:
        h = fp.next()

    min_value = float(range_min) if range_min else None
    max_value = float(range_max) if range_max else None

    for l in fp:
        if len(l) != 2:
            raise ValueError("Bad number of items in line: " + str(l))

        (k, v) = (l[0], float(l[1]))

        values[k].append(v)

        # Update minimum and maximum values, later to be used in the range of the histograms
        if not range_min:  # only if the range wasn't given as a parameter
            if not min_value:
                min_value = v
            elif min_value > v:
                min_value = v

        if not range_max:
            if not max_value:
                max_value = v
            elif max_value < v:
                max_value = v

    plots = sum([len(v) > threshold for v in values.itervalues()])
    i = 1
    plt.figure()
    for k, v in values.iteritems():
        if len(v) > threshold:
            plt.subplot(ceil(plots / float(columns)), int(columns), i)
            if stats:
                k += "\nm=%0.2f,s=%0.2f,med=%0.2f" % (mean(v), std(v), median(v))
            draw_hist(k, v, (min_value, max_value), ylabel="Count", xlabel=h[1])
            if markers:
                plt.axvline(mean(v), color='r', linestyle='-')
                plt.axvline(mean(v)+std(v), color='r', linestyle='--')
                plt.axvline(mean(v)-std(v), color='r', linestyle='--')
                plt.axvline(median(v), color='b', linestyle='-')
            print k.replace('\n', ': \t') + ", Count:" + str(len(v))
            i += 1


    plt.subplots_adjust(hspace=float(vert_space))  # tweak spacing to prevent clipping of x-label
    plt.show()


if __name__ == "__main__":
    try:
        hist_from_file()
    except KeyboardInterrupt:
        pass
