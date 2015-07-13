from bisect import bisect_left
import pickle
from enum import Enum
from matplotlib import pyplot as plt
from numpy import mean, median, std

__author__ = 'omer'

class ZeroBasedEnum(Enum):
    @property
    def zvalue(self):
        return self.value-1

def save_obj(obj, name ):
    '''
    Save pickled object
    :param obj: Object
    :param name: Filename
    '''
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    '''
    Load object from pickle file
    :param name: File name
    :return: Object
    '''
    with open(name, 'rb') as f:
        return pickle.load(f)


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

def draw_hist(title, values, range=None, facecolor=None, ylabel=None, xlabel=None):
    """
    This function draws a histogram on the current plot
    :param title: Title of the histogram
    :param values: List of values to draw the histogram of
    :param range: A range both for the binning and for the drawing
    :param facecolor: The facecolor of the bars
    :param ylabel: ylabel of the histogram ('Count' by default)
    :param xlabel: xlabel of the histogram
    :return: Returns the handle to the histogram
    """
    if not facecolor:
        facecolor = 'green'

    if not ylabel:
        ylabel = 'Count'

    h = plt.hist(values, bins=20, range=range, facecolor=facecolor)
    plt.title("%s" % title)
    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    plt.xlim(range)
    return h


def draw_hist_with_stats(title, values, range=None, facecolor=None, ylabel=None, xlabel=None):
    '''
    calls draw_hist(...) with adds vertical markers for median, mean and standard deviation
    '''
    m = mean(values)
    med = median(values)
    s = std(values)
    max_count = max(h[0])

    h = draw_hist("%s\nmed:%.3g,mean:%.3g,std:%.3g" % (title, med, m, s),
                  values, range, facecolor, ylabel, xlabel)

    plt.axvline(m, color='r', linestyle='-')
    plt.axvline(m+s, color='r', linestyle='--')
    plt.axvline(m-s, color='r', linestyle='--')
    plt.axvline(med, color='b', linestyle='-')

    plt.annotate("%0.4g" % m, xy=(m, max_count-5))
    plt.annotate("%0.4g" % (m+s), xy=(m+s, max_count-5))
    plt.annotate("%0.4g" % med, xy=(med, max_count-8))
    # plt.annotate('mean', xy=(m, max_count), xytext=(m-0.2, max_count+5),
    #     arrowprops=dict(facecolor='black', shrink=0.05))

    # Prettify
    plt.subplots_adjust(left=0.15) # tweak spacing to prevent clipping of y-label
    return h
