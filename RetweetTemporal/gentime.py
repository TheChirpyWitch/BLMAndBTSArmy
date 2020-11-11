import pandas as pd
l=(pd.DataFrame(columns=['NULL'],
index=pd.date_range('2020-06-07T13:00', '2020-06-07T23:00', freq='15T'))
.index.strftime('%Y-%m-%d %H:%M').tolist())
print(l)

for s in l:
    str="rule = gen_rule_payload(query, results_per_call=100, from_date='{}')".format(s)
    print (str)

