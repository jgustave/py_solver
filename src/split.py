import pandas as pd
import os

#Split the 4 output files in to subdirectories with 1 file per ['marketing_channel','tactic','campaign']


pvars = ['ad_spend','clicks']

for f in pvars :
    #read
    raw = pd.read_csv( '/tmp/p_'+f+'.csv', index_col=False)

    #create dir
    if not os.path.exists('/tmp/'+f):
        os.mkdir('/tmp/'+f)

    #split
    ans = [y for x, y in raw.groupby(['marketing_channel'], as_index=False) ]

    #Write output
    for a in ans:
        mc=a.iloc[0]['marketing_channel']
        #tactic=a.iloc[0]['tactic']
        #campaign=a.iloc[0]['campaign']

        #Dropping tactic for now because it is duplicated in the data for some reason.. tactic contains business_category
        a.drop(columns=['marketing_channel','tactic'])\
            .sort_values(['customer_type','location','product_category','business_category','order_channel'])\
            .to_csv('/tmp/'+f+'/' + mc + '.csv', index=False)

#Split only on marketing_channel.


#(Demand Drivers)
#FB and DV360
#Marketing promotions ... (What if for all category?)




