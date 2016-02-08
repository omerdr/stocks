To create prediction matrix:
============================

1. Run 'scrape_marketbeat_recommendations.py' to get the new analyst predictions.

    This will create 'marketbeat_nasdaq.csv'. 
    Note they only keep about 2 years in the past, and that's also somewhat diluted, so better to use a file that was 
    generated a while back (we normally want their predictions from over a year ago to compare to the results a year 
    later).
    
2. Run 'download_all_tickers.sh'.

    This will mine Yahoo! Finance for stocks prices and create 'historical_data'.
    
3. Run 'merge_analysts_with_quotes.py'

    This will take the analyst prediction file and the stock prices and combine them into a single file with:
    'Ticker, Firm, Action, Date, Old_Target, New_Target, Target_Ratio, EOQ_Price, Price_EOQ_next_year, Price_Ratio'.    
    Which can be used to create the final matrix
    
4. Run 'structure_data_matrix_for_regression.py'
    
    This will output 'data_matrix.mat' with everything that's need.
    A little more parsing is still required, and is done using 'parse_data_matrix.m'
    
5. Run 'parse_data_matrix.m'
    
    This will separate the data matrix Z, the true response vector y, and the labels.

Files
=====

## scrape_marketbeat_recommendations.py
    Python code for scraping marketbeat.com for analyst recommendations.
    This is the faster way to go to get the marketbeat analyst recommendations.
    The output is a large file with the fields: Ticker, Research Firm, Action, Recommendation, Price Change    

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
    
## merge_analysts_with_quotes.py
    A newer version of price_change_hist.py, cleaned up (uses myutils and financial_utils) and added support for
    start/end of quarter quotes (instead of current date and precisely a year from now). This support allows creating
    a baseline for comparing analyst recommendations.
    
## draw_distributions.py
    one of the outputs of price_change_hist.py is a pickle saved to ranking.pkl, that contains a dict where the keys
    are the status (buy/sell/etc), and the value is a list of all the percentage changes a year from the recommendation.
    draw_distributions.py takes this dict and creates images of the histograms of the change that follows every the 
    prediction of the analyst a year from the prediction.
    
## draw_distributions_per_analyst.py

## hist_from_file.py
    Gets comma separated key-value pairs, and plots hist of the values for every key 
    (given more than threshold occurrences). Very useful utility.
    
## normalize_field.py
    Gets csv file as input, and adds another field at the end of every line with the v/sum(v), where v is the value at
    'value-field' and the sum is over all the values with the same key (specified by 'key-field').
    Also a very useful utility for functions that are a bit too verbose with awk (now also supports count & average).

## draw_price_change_accuracy_hists.py
    Draws a histogram of Accuracy (|New Price - Target| / |Original Price|)


## ordereddefaultdict.py
    An implementation of OrderedDefaultDict taked from 
    http://stackoverflow.com/questions/4126348/how-do-i-rewrite-this-function-to-implement-ordereddict/4127426#4127426
    OrderedDefaultDict allows to create an ordered dictionary with a default type so we don't have to worry about 
    initialization when placing a list (for instance) inside the dict.

## filter-top-20-analysts.sh
    Shell script for taking the analysts with the most recommendations (top 20), and creating a separate recommendation
    file for each under data/top20_analysts.csv.
    
## data/marketbeat_baseline_SOQ_EOQ_price_target_change.csv
    Contains analyst recommendations with actual price changes. For every recommendations, the quotes given in this 
    file are from the start of the corresponding quarter (SOQ) to the end of the same quarter in the following 
    year (EOQ).
    This file was generated using:
    ```python merge_analysts_with_quotes.py --historical-quotes-dir=historical-quotes data/marketbeat_nasdaq.csv > data/marketbeat_baseline_SOQ_EOQ_price_target_change.csv```