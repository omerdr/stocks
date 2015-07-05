from twisted.internet import defer, reactor
from twisted.web.client import getPage
import time

def processPage(page, url):
    # do somewthing here.
    return url, len(page)

def printResults(result):
    for success, value in result:
        if success:
            print 'Success:', value
        else:
            print 'Failure:', value.getErrorMessage()

def printDelta(_, start):
    delta = time.time() - start
    print 'ran in %0.3fs' % (delta,)
    return delta

urls = [
    'http://www.google.com/',
    'http://www.lycos.com/',
    'http://www.bing.com/',
    'http://www.altavista.com/',
    'http://achewood.com/',
]

def fetchURLs():
    callbacks = []
    for url in urls:
        d = getPage(url)
        d.addCallback(processPage, url)
        callbacks.append(d)

    callbacks = defer.DeferredList(callbacks)
    callbacks.addCallback(printResults)
    return callbacks

def done(a):
    print "Stopping..."
    reactor.stop()

@defer.inlineCallbacks
def main():
    times = []
    for x in xrange(5):
        d = fetchURLs()
        d.addCallback(printDelta, time.time())
        times.append((yield d))
    print 'avg time: %0.3fs' % (sum(times) / len(times),)
    d.addBoth(done)



reactor.callWhenRunning(main)
reactor.run()