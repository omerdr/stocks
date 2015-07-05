import pandas as pd
from IPython.core import pylabtools
import matplotlib
from actions_naming import marketbeat_mapping

# STOCKS_FILE_NAME = 'data/marketbeat_nasdaq_latest.csv'
STOCKS_FILE_NAME = 'data/marketbeat_nasdaq_2013_only.csv'
OUTPUT_NUMERIC_RECOS_FILE_NAME = 'data/marketbeat_numeric_recos_2013.csv'

# global drawing options
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
matplotlib.rcParams['mathtext.fontset'] = 'cm' # deals with missing fonts in matplotlib
pylabtools.figsize(15, 5)

def construct_data_matrix(data, output_file_name):
    # Add a column with the date string converted to datetime
    data['DateTime'] = pd.to_datetime(data['Date'])

    # filter the latest recommendation from every analyst and every ticker
    latest = data.iloc[data.groupby(['Ticker', 'Firm']).DateTime.idxmax()]

    # Sanity check - see that 4 actions turned into only the latest
    print data[(data['Ticker'] == 'MSFT') & (data['Firm'] == 'Goldman Sachs')]
    print '\n\n'
    print latest[(latest['Ticker'] == 'MSFT') & (latest['Firm'] == 'Goldman Sachs')]

    # Pivot the table, each row is a firm, each column a ticker, and the value of each cell is the rating
    recos = latest.pivot('Firm','Ticker','Rating').dropna(how = 'all') # ALL rows = NaN

    # print a sample
    # just show firms that have recommendations on all
    print recos[['FB','MSFT','TSLA','AMZN','NFLX']].dropna(how='any').fillna('')

    # print data.Rating.unique()
    # print pd.Series(recos.values.ravel()).unique()

    numeric_recos = recos.fillna('Neutral')
    numeric_recos.replace('(.*\s*->\s*)(?P<to>.*)', '\\g<to>', regex=True, inplace=True) # remove '.*->'
    numeric_recos.replace(marketbeat_mapping, inplace=True) # map text to +1,0,-1
    numeric_recos = numeric_recos.convert_objects(convert_numeric=True) # now convert the types
    numeric_recos.to_csv(output_file_name)


def main():
    data = pd.read_csv(STOCKS_FILE_NAME, parse_dates=True)
    print data[:5]

    construct_data_matrix(data, OUTPUT_NUMERIC_RECOS_FILE_NAME)

if __name__ == "__main__":
    main()