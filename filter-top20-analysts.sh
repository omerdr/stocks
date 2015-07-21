# to run on the top 20 analysts:
# take top 20 analysts:
# cat data/marketbeat_nasdaq.csv | python parse_csv.py | awk -F, '{ print $3 }' | sort | uniq -c | sort -nr | head -20
# choose only the analyst's name and grep the relevant data
# | awk '{ $1=""; sub(/^\s+/,"",$0); print $0; }' | parallel "grep {} data/marketbeat_nasdaq.csv > data/top20_analysts/{}.csv"
# all in all:
cat data/marketbeat_nasdaq.csv | python parse_csv.py | awk -F, '{ print $3 }' | sort | uniq -c | sort -nr | head -20 | awk '{ $1=""; sub(/^\s+/,"",$0); print $0; }' | parallel "grep {} data/marketbeat_nasdaq.csv > data/top20_analysts/{}.csv"

