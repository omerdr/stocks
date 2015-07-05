'''
The splitting of analyst recommendations into labels.
Yahoo! Finance is split into 3 dicts - buy, sell and neutral.

yahoo_mapping is a dictionary that maps the text into +1,-1 and 0 (respectively).

'''

yahoo_buy = ['Buy', 'Outperform', 'Overweight', 'Strong Buy', 'NT Buy/LT Buy', 'Top Pick', 'Long-term Buy', 'LT Buy',
 'NT Neutral', 'Accumulate', 'Above Average', 'Add', 'Recommended List', 'Outperf. Signif.', 'NT Accum/LT Buy', 'Mkt Outperform',
 'Positive', 'Attractive', 'NT Accumulate', 'NT Buy', 'Sector Outperform', 'Over Weight', 'LT Attractive', 'Mkt Outperformer',
 'Market Outperform', 'LT Strong Buy', 'NT Strong Buy', 'Buy Aggressive', 'NT Accum', 'Aggressive Buy', 'Recomm List', 'Trading Buy',
 'LTerm Buy', 'NT Accum/LT Accum', 'Buy $50', 'ST Accumulate', 'NT Outperform', 'Outperform/Buy', 'ST Mkt Perform/LT Buy', 'NT/LT Strong Buy',
 'LT Mkt Outperformer', 'Focus Stock', 'LT Accumulate', 'Sector Outperformer', 'Strong Buy Aggress', 'Strong Buy Spec', 'LT Accum', 'Net Positive',
 'Trading buy', 'Long Term Buy', 'ST Buy/LT Buy', 'IT/LT Outperform', 'Recomm. List', 'Buy - Long-Term', 'IT Outperform', 'NT/LT Buy',
 'ST/LT Buy', 'Buy $32', 'NT/LT Outperformer', 'Outperform Signif', 'IT/LT Mrk Perform', 'US Recomm. List', 'ST Buy', 'Buy-Focus List',
 'Source of Funds', 'ST Mkt Outperform', 'Focus List', 'Outperform Sig', 'Speculative Buy', 'Spec. Buy', 'NT/LT Accum', 'NT Outperformer',
 'Outperformer', 'NT Neutral/LT Accum', 'Strong Buy $100', 'IT Accum/LT Buy', 'NT Strong Buy/LT Buy', 'Strong Buy $70', 'Buy/Aggr', 'NT Buy/LT Accum',
 'Attrac LT', 'Buy $60', 'accumulate', 'Buy Speculative', 'IT Outperformer', 'ST Buy/LT Mkt Perform', 'BUY - Long-Term', 'Strong Buy $50',
 'Mrk Outperform', 'Buy $18', 'ST/LT Mkt Outperform', 'LT Outperform', 'Outperf Signif', 'IT Buy/LT Strg Buy', 'NT Acc/LT Buy', 'Outperform $55',
 'SB', 'Stong Buy', 'Buy-Aggresive', 'Strong Buy $40', 'Buy $100', 'NT Buy/LT Strong Buy', 'Strong Buy $111', 'ST Hold/LT Buy',
 'Buy/Spec', 'Buy $75', 'IT Buy', 'Sell Short', 'NT Accu/LT Buy', 'IT Strong Buy', 'Buy/Core', 'Strong Buy $30',
 'NT Strong Buy/LT Strong Buy', 'Reccomended List', 'Industry Outperform', 'NT/LT Outperfrm', 'Strong Speculative Buy', 'Buy $16', 'Outprf Signif', 'Over-weight',
 'NT Mkt Outperfor', 'LT Mkt Outperform', 'Thematic Opportunity', 'Strong Buy $255', 'NT Accum/ LT Buy', 'IT Mkt Pfm/LT Outp', 'Strong buy', 'LT Hold',
 'NTAccumulate', 'IT/ Outperform', 'Buy $90', 'Gradually Accumulate', 'ST Strong Buy', 'Outprf Signif.', 'Buy/High Risk', 'Mkt Outperform $23',
 'NT/LT Accumulate', 'Mkt Outprfm', 'NT/LT Outperform', 'ST Buy/LT Outprf', 'Buy $52', 'St Buy/Buy', 'Long Term Accumulate', 'NT Buy/ LT Buy',
 'NTBuy', 'Outperfm Signif', 'NT Accumulate/LT Buy', 'NT Accm/LT Buy', 'Buy-Spec', 'NT Acc/ LT Buy', 'ST Accum/LT Buy', 'NT LT Buy',
 'NT Mkt Outperformer', 'Buy $26', 'NT Buy/LT Neutral', 'Buy $35', 'Strong Buy Agg', 'Buy/Aggressive', 'IT Mkt Outperf', 'Buy $62',
 'Buy $29', 'IT Accumulate', 'Buy/Speculative', 'Strong Buy/Avg', 'NT/LT  Buy', 'Outperfrm Signif', 'Attractive $22', 'Long-term Accumulate', 'Outperform Signi', 'ITAccm/LTBuy']

yahoo_neutral = ['Neutral', 'Market Perform', 'Equal Weight', 'Mkt Perform', 'Hold', 'Sector Perform', 'Peer Perform', 'Equal-weight',
'In-Line', 'Average', 'Underweight', 'Perform In Line', 'Maintain', 'Perform', 'Fair Value', 'In-line',
'NT Neutral/LT Neutral', 'Mkt Performer', 'LT Mkt Perform', 'NT Mkt Perform', 'Perform-In-Line', 'NT Reduce-Sell/LT Buy', 'NT Neutral/LT Buy', 'NT Reduce-Sell/LT Neutral',
'NT Hold', 'LT Neutral', 'Maintain Position', 'NT Market Perform', 'ST/LT Mkt Perform', 'IT Mkt Perform', 'In Line', 'LT Mkt Performer',
'NT Mkt Performer', 'Equal-Weight', 'Not Rated', 'Market Weight', 'ST Neutral', 'ST Mkt Perform', 'Net Neutral', 'Mkt Neutral',
'NT Neut/LT Buy', 'NT Nuet/ LT Accum', 'NT Ntrl/LT Accm', 'NT Neut/LT Accum', 'NT/LT Neutral', 'NT Ntrl/LT Accum', 'Monitor', 'NT Ntrl/LT Buy',
'NT Mkt Prfm/LT Outprfm', 'Action Call Pos', 'ST Hold', 'LT Mkt Perforn', 'LT Market Perform', 'NT Rduce/LT Ntrl', 'NT Reduce/LT Neut', 'Sector Performer',
'ST Mkt Perform/LT Mkt Perform', 'Market Performer', 'IT', 'Watch List', 'Neutral $23', 'Hold/Neutral', 'Neutral $64', 'NT Neutral/LT Strong Buy',
'NT Mkt Prfm/LT', 'NT Neut/LT Neut', 'NT/LT Mkt Performer', 'ST Avoid/LT Mkt Perform', 'Industry Perform', 'Cautious', 'Mkt  Perform', 'ST/LT Mkt',
'Core Neutral', 'ST Mkt Prfrm/LT Mkt Otprfrm', 'IT/LT Mkt Pfm', 'Specultv Neutral', 'New', 'NT Mkt Pfm/LT Outp', 'NT Neutral/LTBuy', 'ST Neutral/LT Buy',
'Hold $4', 'Buy/Avg', 'Neutral $70', 'Mrk Perform', 'NT Neut/ LT Accum', 'Perf.-in-Line', 'NT/LT Hold', '-',
'IT Mrkt Perform', 'No Rating', 'IT/LT Mkt Prfrm', 'Neutral/Avg', 'NT Nuet/ LT Buy', 'NT neutral', 'NT Accum/LT Neut', 'Prfrm-In-Line',
'Mkt Perform $60', 'IT Mkt Performer', 'neutral', 'ST Buy/LT Hold', 'Affirm', 'Nuetral', 'NT Ntrl/LT Attra', 'IT/LT Mkt Pfrm',
'NT Neut/ LT Buy', 'Neutral/Average', 'NT Neut/ LT Neut', 'NT Reduce/LT Reduce', 'NB Montgomery']

yahoo_sell = [ 'Sell', 'Underperform', 'Reduce', 'Mkt Underperform', 'Unattractive', 'Sector Underperform', 'Below Average', 'Avoid',
'ST Mkt Underperform', 'Negative', 'Strong Sell', 'Under Weight', 'NT Reduce', 'Net Negative', 'Under Perform', 'Reduce/Sell',
'NT Reduce/Sell', 'ST Underperform', 'ST Avoid', 'NT Underperform', 'ST Avoid/LT Avoid', 'IT Underperform', 'Swap', 'Market Underperform',
'Action Call Neg', 'Under-weight', 'NT Reduce-Sell/LT Reduce-Sell', 'Industry UnderPerform', 'Mkt Underperformer', 'LT Reduce/Sell', 'Avoi', 'Sector Underperformer' ]

#
# ETH MSC THESIS USED THE FOLLOWING DEFINITIONS
# Buy
# Above Average, Accumulate, Add, Attractive, Buy, Buy Aggressive, Buy Speculative,
# IT Outperform, LT Accum, LT Accumulate, LT Attractive, LT Buy, LT Mkt Out-
# performer,  LT Outperform,  LT Strong Buy,  Market Outperform,  Mkt Outperform,
# Mkt Outperformer, Net Positive, NT Accum, NT Accum/LT Accum, NT Accum/LT
# Buy, NT Accumulate, NT Buy, NT Buy/LT Buy, NT Buy/LT Strong Buy, NT Mkt
# Outperformer, NT Outperformer, NT Strong Buy, NT Strong Buy/LT Strong Buy,
# NT/LT Accum, NT/LT Buy, NT/LT Outperformer, NT/LT Strong Buy, Outperform,
# Outperform/Buy, Over Weight, Overweight, Positive, Recomm List, Recomm:List,
# Recommended List, SB, Sector Outperform, Speculative Buy, ST Buy, ST Buy/LT
# Buy, Strong Buy, Strong Buy Aggress, Strong Buy Spec, Top Pick
#
# Neutral
# Average,  Equal  Weight,  Equal-weight,  Hold,  In-line,  IT  Mkt  Perform,  LT  Market
# Perform,  LT  Mkt  Performer,  LT  Mkt  Perforn,  Maintain,  Maintain  Position,  Mar-
# ket  Perform,  Market  Weight,  Mkt  Perform,  Neutral,  NT  Mkt  Performer,  NT  Mkt
# Prfm/LT Outprfm, NT Neutral, NT Neutral/LT Buy, NT Reduce/LT Neut, NT/LT
# Mkt Performer, NT/LT Ntrl, Peer Perform, Perform, Sector Perform, ST Mkt Per-
# form, ST Mkt Perform/LT Mkt Perform, Under Review
#
#
# Sell
# Avoid,  Below  Average,  Market  Underperform,  Mkt  Underperform,  Negative,  NT
# Reduce-Sell/LT  Neutral,  NT  Reduce/Sell,  Reduce,  Sector  Underperform,  Sell,  ST
# Avoid, ST Avoid/LT Avoid, Strong Sell, Unattractive, Under Weight, Underperform,
# Underweight

# mapping = {"NA":0.0 ,"Buy" :1.0,"Neutral":0.5}
yahoo_mapping = {}

for t in yahoo_buy:
    yahoo_mapping[t] = 1.0

for t in yahoo_neutral:
    yahoo_mapping[t] = 0.0

for t in yahoo_sell:
    yahoo_mapping[t] = -1.0



marketbeat_buy = ['Buy', 'Positive', 'Overweight', 'Strong-Buy', 'Outperform', 'Market Outperform', 'BUY',
                  'Sector Outperformer', 'Sector Outperform', 'Top Pick', 'Focus Stock', 'Exemplary',
                  'Conviction Buy List', 'Focus List', 'Conviction-Buy', 'Accumulate', 'Best Ideas List',
                  'add', 'Speculative Buy']

marketbeat_sell = ['Sell', 'Underweight', 'Reduce', 'Under Perform', 'Sector Underperformer', 'Strong Sell',
                   'Market Underperform', 'Sector Underperform', 'Negative', 'Priority List', 'Poor', 'Underperform']

marketbeat_neutral = ['Neutral', 'Hold', 'In-Line', 'Market Perform', 'Fairly Valued', 'Equal Weight', 'Average',
                      'Sector Perform', 'Sector Performer', 'Fair Value', 'line', 'Mkt Perform', 'Sector Weight',
                      '$37',  'Standard', 'HOLD', 'R', 'Not Rated', 'Peer Perform']

marketbeat_mapping = {}

for t in marketbeat_buy:
    marketbeat_mapping[t] = 1.0

for t in marketbeat_neutral:
    marketbeat_mapping[t] = 0.0

for t in marketbeat_sell:
    marketbeat_mapping[t] = -1.0
