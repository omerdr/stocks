# <codecell>

import requests
import csv
from BeautifulSoup import BeautifulSoup as bs
import scipy.io as sio

MARKETBEAT_NASDAQ_URL = 'http://www.marketbeat.com/stocks/NASDAQ/{0}'
MARKETBEAT_NASDAQ_MOST_RECENT_URL = 'http://www.marketbeat.com/stocks/NASDAQ/{0}/?MostRecent=1'

# <codecell>

def get_ranking_csvrows_from_url(url, headers=None):
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
    if table == None:
        raise Exception('No table in page')
        
    cur_headers = table.findAll('th') #,{'class':'header'})
    if cur_headers == None: 
        raise Exception('Headers not found')

    cur_headers = [ h.text.strip() for h in cur_headers ]
    cur_headers.insert(0,u'Ticker')

    if None != headers and headers != cur_headers:
        raise Exception('Wrong headers found', str(cur_headers))
    
    data = table.findAll('td') #,{'class':'yfnc_tabledata1'})

    it = iter([ d.text.strip() for d in data ]) # create an iterator over the textual data
    csvrows = zip([tick]*(1+len(data)/5),it,it,it,it,it,it) # each call to it returns the next data entry, so this zip will create a 6-tuple array

    # dirty trick (only return 2 parameters if we don't know what we're looking for):
    if None == headers:
        ret = csvrows, cur_headers
    else:
        ret = csvrows

    return ret

# <codecell>

tick = 'INTC'
csvrows,headers = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick))

# THIS SHOULD THROW AN EXCEPTION
tick = 'AAME'
try:
    csvrows = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick),headers)
except Exception as e:
    print 'SUCCESS'
    print e
else:
    print 'FAIL'

# <codecell>

print "\t".join(headers)
print "\t".join(csvrows[0])

# <codecell>

print len(csvrows)
print len(headers)
print "\t".join(csvrows[0])
print "\t".join(csvrows[1])

# the last cell is unneeded html code, we'll get rid of it later

# <headingcell level=3>

# And here's a loop for getting data on all the tickers from 'nasdaq.txt' and writing them to 'marketbeat_nasdaq.csv'

# <rawcell>

# First line up all the tickers that we want to extract

# <codecell>

with open('NASDAQ.txt','r') as f:
    lines = f.readlines()

tickers = [l.strip() for l in lines if l.strip() != '']
# tickers

# <rawcell>

# Then extract everything that's needed

# <codecell>

out = open('data/marketbeat_nasdaq.csv','a')
csvout = csv.writer(out)

headers = None
for i,tick in enumerate(tickers[1:]):
    tick = tick.split('\t')[0]
    print i,tick,',',
    try:
        if headers == None:
            csvrows,headers = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick))
        else:
            csvrows,_ = get_ranking_csvrows_from_url(MARKETBEAT_NASDAQ_URL.format(tick),headers)
        csvrows = [ r[:-1] for r in csvrows ] # get rid of the last element in every tuple
    except Exception as inst:
        print inst
        continue

    csvout.writerows(csvrows)

out.flush()
out.close()
# csvout.close()
# close(out)

# <rawcell>


# <codecell>

# with open('stocks.csv','r') as infile:
#     csvin = csv.reader(infile)
#     data = map(tuple,csvin)
#
# # <rawcell>
#
#
# # <codecell>
#
# data[len(data)-1]
#
# # <rawcell>
#
#
# # <codecell>
#
# sio.savemat('stocks.mat',{'data':data},do_compression=True)
#
