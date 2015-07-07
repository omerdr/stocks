Files
=====

## scrape-with-twisted.py:
    Python code for scraping marketbeat.com for analyst recommendations.
    Code written using twisted and the scraping is done using the reactor design pattern.
    The output is a large file with the fields: Ticker, Research Firm, Action, Recommendation, Price Change

## structure-data-matrix.py:
    Take the scraped data, and pivot it to get a proper data matrix, where each row represents an analyst (predictor),
    and each column represents a ticker. The contents of each cell will be 1 for buy, -1 for sell and 0 for neutral or
    no recommendation.
    
## (NASDAQ|LSE|NYSE).txt:
    A list of tickers to be mined from these stock exchanges.
    
## action-naming.py:
    Rules for clustering the analyst recommendation strings into buy/neutral/sell.
    
## parse_csv.py:
    Reads a csv from stdin and writes the csv to stdout after parsing the fields and replacing every ',' in the text
    with a ';' (only within the text fields, not in-between fields).
    This way csv files can be parsed with awk.
    
## order-recommendations.py
    Takes in upgrade and downgrade recommendations and figures out the ordinal structure of the rankings used by 
    analysts. E.g. upgrade from perform to outperform means that outperform is more than perform. The output is the
    graph structure of the rankings.
    
## price_change_hist.py
    Taking in recommendations and prices and outputs a histogram. For every type of recommendation (buy/sell/etc), what
    was the price change a year after the recommendation was given (in percentage).
    
## draw_distributions.py
    one of the outputs of price_change_hist.py is a pickle saved to ranking.pkl, that contains a dict where the keys
    are the status (buy/sell/etc), and the value is a list of all the percentage changes a year from the recommendation.
    draw_distributions.py takes this dict and creates images of the histograms of the change that follows every the 
    prediction of the analyst a year from the prediction.

## ordereddefaultdict.py
    An implementation of OrderedDefaultDict taked from 
    http://stackoverflow.com/questions/4126348/how-do-i-rewrite-this-function-to-implement-ordereddict/4127426#4127426
    OrderedDefaultDict allows to create an ordered dictionary with a default type so we don't have to worry about 
    initialization when placing a list (for instance) inside the dict.

## filter-top-20-analysts.sh
    Shell script for taking the analysts with the most recommendations (top 20), and creating a separate recommendation
    file for each under data/top20_analysts.csv.