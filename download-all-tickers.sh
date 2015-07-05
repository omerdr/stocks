
# multi threaded download of all NASDAQ historical data from Yahoo! Finance
cat NASDAQ-only-tickers.txt | pv | awk '{ print "curl \"real-chart.finance.yahoo.com/table.csv?s="$1"&a=0&b=1&c=2013&g=d&ignore=.csv\" > historical-quotes/"$1".txt" }' | parallel -j 8

# write the headers to all.csv
head -1 GOOG.txt  > all.csv

# skip the header line in every file, and concatenate all the files into one big file with all the data
# remember to insert the file name (which is the ticker) into the first field in every row
awk '{ if (FNR > 1) { sub(".txt","",FILENAME); print FILENAME,",",$0; } }' *.txt >> all.csv

# grep only January and December of 2014
cat all.csv | grep '2014\-01\-\|2014\-12\-' > jan-dec-2014.csv

# take the first and last line of every ticker (assuming they are ordered this is the first and last quote of the year)
cat jan-dec-2014.csv | awk -F, '{ if (t!=$1) { if (l!="") {print l;} print $0; t=$1; }; l=$0; } END {print $0}' > tmp.csv

echo "Year End Ticker,Year End Date,Year End Open,Year End High,Year End Low,Year End Close,Year End Volume,Year End Adj Close,Year Start Ticker,Year Start Date,Year Start Open,Year Start High,Year Start Low,Year Start Close,Year Start Volume,Year Start Adj Close" > 2014-open-close.csv

# merge every 2 lines
cat tmp.csv | paste - - -d, >> 2014-open-close.csv

# take only the prices
cat 2014-open-close.csv | awk -F, '{ print $1","$2","$8","$9","$10","$11}' > 2014-open-close-price.csv

# create the 2014 price-movement file. 1 for up, -1 for down
echo "Ticker,Price Movement,Year Open, Year Adj Close" > 2014-up-down.csv
awk 'FNR > 1' 2014-open-close-price.csv | awk -F, '{ if ($3 > $6) print $1,1,$6,$3; else print $1,-1,$6,$3; }' >> 2014-up-down.csv
