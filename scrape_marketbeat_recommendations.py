import requests
import csv
import errno

import sys
from BeautifulSoup import BeautifulSoup as bs

MARKETBEAT_NASDAQ_URL = 'http://www.marketbeat.com/stocks/NASDAQ/{0}'
MARKETBEAT_NASDAQ_MOST_RECENT_URL = 'http://www.marketbeat.com/stocks/NASDAQ/{0}/?MostRecent=1'

NASDAQ_TICKER_LIST_FILE = 'NASDAQ.txt'
OUTPUT_FILE = 'data/marketbeat_nasdaq_test.csv'


def get_ranking_csvrows_from_url(url, tick, headers=None):
    '''
    get_ranking_csvrows_from_url requests the page from the url given and looks for
    the table with the data.
    Special care is given for when we know which data we want to get (kind of a workaround)
    so that the first call to the function will return the appropriate headers, and any
    subsequent call should pass the headers and this function will make sure that the returned
    data corresponds to the correct format (the correct data in each cell).
    The function will raise an exception if it's the wrong format.
    NOTE: Exceptions should and will be raised on some of the stocks. Marketbeat's website has
    an invisible table inside the 'no-data' pages. These tables are wrongly recognized as the
    actual table (because they have the same id), but the headers verification finds the problem
    and circumvents it.

    :param url: Marketbeat Nasdaq recommendations URL to be used for scraping
    :param tick: The ticker name of the stock that we are scraping (e.g. GOOG, AAPL, MSFT)
    :param headers: The fields that need to be scraped from the given URL. The first call to the function will populate
                    this string.
    '''
    try:
        page = requests.get(url)
    except Exception as inst:
        raise inst
    soup = bs(page.text)

    table = soup.find(lambda tag: tag.name == 'table' and
                                  tag.has_key('id') and
                                  tag['id'] == 'ratingstable' and
                                  tag.has_key('class') and
                                  tag['class'] == "tablesorter")
    if table is None:
        raise Exception('No table in page')

    cur_headers = table.findAll('th')  # ,{'class':'header'})
    if cur_headers is None:
        raise Exception('Headers not found')

    cur_headers = [h.text.strip() for h in cur_headers]
    cur_headers.insert(0, u'Ticker')

    if headers is not None and headers != cur_headers:
        raise Exception('Wrong headers found', str(cur_headers))

    data = table.findAll('td')  # ,{'class':'yfnc_tabledata1'})

    it = iter([d.text.strip() for d in data])  # create an iterator over the textual data
    csvrows = zip([tick] * (1 + len(data) / 5), it, it, it, it, it,
                  it)  # each call to it returns the next data entry, so this zip will create a 6-tuple array

    # dirty trick (only return 2 parameters if we don't know what we're looking for):
    if headers is None:
        ret = csvrows, cur_headers
    else:
        ret = csvrows

    return ret


def scrape_marketbeat_recommendations():
    # First: Do some testing to see the website hasn't changed (much)
    tick = 'INTC'
    try:
        csvrows, headers = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick), tick)
        print "Headers for scraping are:\t" + ", ".join(headers)
        print "Original headers were:   \tTicker, Date, Firm, Action, Rating, Price Target, Actions"
        print "Sample data:             \t" + ", ".join(csvrows[0])
        print "\nNumber of csv rows retrieved (stock actions for INTC): " + str(len(csvrows))
        print '\t'.join(csvrows[0])
        print '\t'.join(csvrows[1])

    except Exception as e:
        print 'Problem retrieving headers'
        print e.message

    # THIS TICKER SHOULD THROW AN EXCEPTION
    tick = 'AAME'
    try:
        csvrows = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick), tick, headers)
    except Exception as e:
        print 'Test error handling: SUCCESS'
        # print e
    else:
        print 'Test error handling: FAIL'

    # Now: Get data on all the tickers
    raw_input("Press any key to start scraping...")

    # First line up all the tickers that we want to extract
    with open(NASDAQ_TICKER_LIST_FILE, 'r') as f:
        lines = f.readlines()

    tickers = [l.strip() for l in lines if l.strip() != '']

    out = open(OUTPUT_FILE, 'a')
    csvout = csv.writer(out)

    headers = None
    for i, tick in enumerate(tickers[1:]):
        tick = tick.split('\t')[0]
        print i, tick, ',',
        try:
            if headers is None:
                csvrows, headers = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick), tick)
            else:
                csvrows = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick), tick, headers)
            csvrows = [r[:-1] for r in csvrows]  # get rid of the last element in every tuple
        except Exception as inst:
            print inst
            continue

        csvout.writerows(csvrows)

    out.flush()
    out.close()


if __name__ == "__main__":
    try:
        scrape_marketbeat_recommendations()
    except KeyboardInterrupt:
        pass
    except IOError, e:
        if e.errno != errno.EPIPE:
            raise e
