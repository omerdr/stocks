# <codecell>

from twisted.python.util import println
from twisted.internet import reactor,defer
from twisted.web.client import getPage
from twisted.python.failure import Failure
import csv
from BeautifulSoup import BeautifulSoup as bs
from sys import stderr

#MARKETBEAT_NASDAQ_URL = 'http://www.marketbeat.com/stocks/NASDAQ/{0}'
MARKETBEAT_NASDAQ_MOST_RECENT_URL = 'http://www.marketbeat.com/stocks/NASDAQ/{0}/?MostRecent=1'
MARKETBEAT_NASDAQ_URL = MARKETBEAT_NASDAQ_MOST_RECENT_URL
#OUTPUT_FILE = 'data/tmp.csv' #'data/marketbeat_nasdaq.csv' # append
OUTPUT_FILE = 'data/marketbeat_nasdaq_twisted.csv' # append
NASDAQ_TICKERS_TXT_FILE = 'NASDAQ.txt'

# <codecell>

def parse_html(html):
    '''
    :param html: The HTML response from the website
    :return: The table tag containing all the data
    '''
    soup = bs(html)

    table = soup.find(lambda tag: tag.name == 'table' and
                                  tag.has_key('id') and
                                  tag['id'] == 'ratingstable' and
                                  tag.has_key('class') and
                                  tag['class'] == "tablesorter")
    if table == None:
        raise Exception('No table in page')

    return table

class StaticVars:
    headers = None

def extract_data(table, tick):
    '''
    :param table: The table tag from the web page
    :return: csvrows - a list of tuples with the data from the table. This function also sets StaticVars.headers
    if it wasn't pre-set with the headers of the table. If StaticVars.headers was pre-set, and the headers are different
    from what was retrieved from the table the function will fail.
    '''
    headers = table.findAll('th')
    if headers == None:
        raise Exception('Headers not found')
    headers = [ h.text.strip() for h in headers ]
    headers.insert(0,u'Ticker')

    if StaticVars.headers == None:
        StaticVars.headers = headers
    elif StaticVars.headers != headers:
        raise Exception('Bad headers in page')

    data = table.findAll('td')

    # create an iterator over the textual data
    it = iter([ d.text.strip() for d in data ])

    # each call to it returns the next data entry, so this zip will create a 6-tuple array
    csvrows = zip([tick]*(1+len(data)/5),it,it,it,it,it,it)
    csvrows = [ r[:-1] for r in csvrows ]  # get rid of the last element in every tuple
    #raise Exception("Uh, oh")
    return csvrows

def write_to_file(rows, csvoutfile):
    csvoutfile.writerows(rows)

def printerr(failure):
    failure.trap(Exception)
    try:
        stderr.write("Error while parsing: " + failure.value.message + '\n')
    except:
        stderr.write("Unknown error while parsing\n")

def printResults(result):
    for success, value in result:
        if success:
            print 'Success:', value
        else:
            print 'Failure:', value.getErrorMessage()
    print "Stopping..."
    reactor.stop()


# tick = 'INTC'
# d = getPage(MARKETBEAT_NASDAQ_URL.format(tick))
# d.addCallback(parse_html)
# d.addCallback(extract_data)
# d.addCallback(println)
# d.addErrback(printerr)
#
# reactor.run()


# The Twisted part of the code:
@defer.inlineCallbacks
def main():
    with open(NASDAQ_TICKERS_TXT_FILE,'r') as f:
        lines = f.readlines()

    tickers = [l.strip() for l in lines if l.strip() != '']

    out = open(OUTPUT_FILE,'a')
    csvout = csv.writer(out)

    callbacks = []
    for i,tick in enumerate(tickers[1:]):
        tick = tick.split('\t')[0]
        print i,tick,',',
        d = getPage(MARKETBEAT_NASDAQ_URL.format(tick))
        d.addCallback(parse_html)
        d.addCallback(extract_data, tick)
        d.addCallback(write_to_file, csvout)
        d.addErrback(printerr)
        callbacks.append(d)
        yield d

    callbacks = defer.DeferredList(callbacks)
    callbacks.addCallback(printResults)  # call when done

    out.flush()
    out.close()

reactor.callWhenRunning(main)
reactor.run()