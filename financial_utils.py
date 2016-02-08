import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from myutils import ZeroBasedEnum, find_closest, DatesNotAvailableException
from ordereddefaultdict import OrderedDefaultdict

ANALYST_DATA_HEADER_LINE = 'Ticker,Date,Firm,Action,Rating,Price_Target'
PRICE_CHANGE_HEADER_LINE = \
    'Ticker,Firm,Action,Date,Old_Target,New_Target,Target_Ratio,Current_Price,Price_in_a_year,Price_Ratio'
QUOTES_HEADER_LINE = 'Date,Open,High,Low,Close,Volume,Adj_Close'

ANALYST_DATA_FIELDS = ZeroBasedEnum('ANALYST_DATA_FIELDS', ANALYST_DATA_HEADER_LINE)
PRICE_CHANGE_FIELDS = ZeroBasedEnum('PRICE_CHANGE_FIELDS', PRICE_CHANGE_HEADER_LINE)
QUOT_FIELDS = ZeroBasedEnum('QUOT_FIELDS', QUOTES_HEADER_LINE)

ANALYST_DATA_DATE_FORMAT = '%m/%d/%Y'
PRICE_CHANGE_DATE_FORMAT = '%m/%d/%Y'
QUOT_DATE_FORMAT = '%Y-%m-%d'


def parse_historical_quotes_file(ticker, quotes_dir=None, has_header_line=False):
    if not quotes_dir:
        quotes_dir = os.getcwd()

    with open(os.path.join(quotes_dir, ticker + '.txt'), 'r') as quotes_file:
        quotes = OrderedDefaultdict(list)
        cp = csv.reader(quotes_file)

        try:
            if has_header_line:
                cp.next()  # skip header line
        except StopIteration:
            return None

        for l in cp:
            if len(l) < len(QUOT_FIELDS):
                continue
            quotes[datetime.strptime(l[QUOT_FIELDS.Date.zvalue], QUOT_DATE_FORMAT)] = float(l[QUOT_FIELDS.Adj_Close.zvalue])

        if len(quotes) == 0:
            return None

        return quotes

class FindPrice:
    def __init__(self, quotes_dir, quotes_file_has_header_line=True):
        self._quotes_dir = quotes_dir
        self._has_header = quotes_file_has_header_line

        self._last_ticker = None
        self.quotes = None

    def at(self, ticker, current_date):
        # Cache quotes array to avoid re-reading the file when asked for the same ticker twice in a row
        if ticker != self._last_ticker or not self.quotes:
            # parse the historical quotes file for the given ticker
            self.quotes = parse_historical_quotes_file(ticker, self._quotes_dir, self._has_header)
            self._last_ticker = ticker

        # if the requested date is outside the file's date range raise exception
        if not self.quotes or current_date < self.quotes.keys()[-1] or current_date > self.quotes.keys()[0]:
            raise DatesNotAvailableException

        # return the quote on the closest date within the range
        return float(self.quotes[find_closest(self.quotes.keys(), current_date)])

    _EOQTBL = (((3,31,0),)*3 + ((6,30,0),)*3 + ((9,30,0),)*3 + ((12,31,0),)*3)  # End of quarter lookup table
    def _end_of_quarter(self, ref):
        entry = self._EOQTBL[ref.month-1]  # -1 for zero-based-indexing of arrays, not prior month
        return datetime(ref.year-entry[2], entry[0], entry[1])

    def at_end_of_qtr_next_year(self, ticker, current_date):
        new_date = current_date + relativedelta(years=1)
        new_date = self._end_of_quarter(new_date)
        return self.at(ticker, new_date)

    def at_end_of_qtr(self, ticker, current_date):
        return self.at(ticker, self._end_of_quarter(current_date))

    _SOQTBL = (((1,1,0),)*3 + ((4,1,0),)*3 + ((7,1,0),)*3 + ((10,1,0),)*3)  # End of quarter lookup table
    def at_start_of_qtr(self, ticker, current_date):
        entry = self._SOQTBL[current_date.month-1]  # -1 for zero-based-indexing of arrays, not prior month
        new_date = datetime(current_date.year-entry[2], entry[0], entry[1])
        return self.at(ticker, new_date)
