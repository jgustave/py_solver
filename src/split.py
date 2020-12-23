import pandas as pd
import os

#Split the 4 output files in to subdirectories with 1 file per ['marketing_channel','tactic','campaign']


pvars = ['ad_spend']

for f in pvars :
    #read
    raw = pd.read_csv( '/tmp/'+f+'.csv', index_col=False)

    #create dir
    if not os.path.exists('/tmp/'+f):
        os.mkdir('/tmp/'+f)

    #split
    ans = [y for x, y in raw.groupby(['marketing_channel','tactic','campaign'], as_index=False) ]

    #Write output
    for a in ans:
        mc=a.iloc[0]['marketing_channel']
        tactic=a.iloc[0]['tactic']
        campaign=a.iloc[0]['campaign']
        a.drop(columns=['marketing_channel','tactic','campaign'])\
            .sort_values(['customer_type','location','product_category','business_category','order_channel'])\
            .to_csv('/tmp/'+f+'/' + mc + '___' + tactic + '___' + campaign + '.csv', index=False)





