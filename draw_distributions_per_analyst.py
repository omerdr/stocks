'''
Run with:
cd ~/code/github/stocks/data/top20_analysts
python ../../draw_distributions_per_analyst.py
'''

from math import ceil
from matplotlib import pyplot as plt
import os
import click
from myutils import load_obj, draw_hist_with_stats


def pkl_files(start):
    for root,dirs,files in os.walk(start):
        for name in files:
            if not name.endswith('pkl'):
                continue
            yield (name, "%s/%s" % (root,name))

@click.command()
@click.option('--start-dir', default=os.getcwd(), help='directory to scan pkl files in')
@click.option('--threshold', default=10, help='if there are less than [threshold] number of data points, don\'t draw')
def draw_ranks(start_dir, threshold):
    for title, path in pkl_files(start_dir):
        plt.figure(figsize=(18.0,15.0))
        plt.suptitle(title)
        rank = load_obj(path)
        num_subplots = sum(len(rank[k]) >= threshold for k in rank)

        i = 0
        for k in rank:
            if len(rank[k]) < threshold:
                continue

            print "%s: %d out of %d (row %g, rank %s)" % (path, i, len(rank), ceil(num_subplots/3.0), k)
            plt.subplot(ceil(num_subplots/3.0), 3, i)
            draw_hist_with_stats(k, rank[k], xlabel='1-year Percentage Change')
            i += 1
        plt.show()
        #plt.savefig(title + '.jpg', )
        #plt.close()


if __name__ == "__main__":
    try:
        draw_ranks()
    except KeyboardInterrupt:
        pass
