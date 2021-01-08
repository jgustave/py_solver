from datetime import timedelta, date

#Code generate some SQL.

#Start and end dates
start_date = date(2019, 10, 19)
end_date = date(2020, 10, 30)


delta = timedelta(days=1)
dl = []

while start_date <= end_date:
    dl.append( start_date )
    start_date += delta
    #start_date.strftime("%Y-%m-%d")

#Make date range strings
dstr0 = ''
for d in dl:
    dstr0 += ('"_'+d.strftime("%Y-%m-%d") + '",')
dstr0 = dstr0[0:-1]

dstr1 = '$$VALUES '
for d in dl:
    dstr1 += ("('" + d.strftime("%Y-%m-%d") + "'),")
dstr1 = dstr1[0:-1] + '$$ )'

dstr2 = ''
for d in dl:
    dstr2 += ('"_' + d.strftime("%Y-%m-%d") + '" float,')
dstr2 = dstr2[0:-1]

pvars = ['ad_spend','clicks']

rvars = ['conversions','revenue']

for rvar in rvars:

    basic = '''copy (select customer_type,'none' as location,product_category,business_category,order_channel,''' + dstr0 + ''' 
    from crosstab( 'select rank() OVER (ORDER BY product_category,business_category) as rn,
		   product_category,business_category,date, ''' + rvar

    b2 = ''' FROM 
		 (select b.category_type as product_category,b.category_nm as business_category,a.date,a.conversions,a.revenue from 
			( select date(event_ts) as date, category_id, sum(orders) as conversions, sum(revenue) as revenue from category_segment_actuals group by 1,2 ) a
			join
			category b on (a.category_id = b.id)
			where b.category_type=''category'') aaa
		 ORDER BY 1',''' + dstr1 + ''' as bfoo
            (rn int,
             product_category text,business_category text,
             ''' + dstr2 + ''' )
         cross join (select distinct order_channel from category_segment_actuals) c
         cross join (values ('new'),('existing')) bbb(customer_type)
        ) to '/tmp/''' + rvar + '''.csv' csv header;'''

    print(basic + b2 + '\n')


#Clicks as Response.
basic = '''copy (select customer_type,'none' as location,product_category,business_category,order_channel,''' + dstr0 + ''' 
from crosstab( 'select rank() OVER (ORDER BY product_category,business_category) as rn,
       product_category,business_category,date, clicks '''

b2 = ''' FROM 
        (select e.category_type as product_category,e.category_nm as business_category, date(a.event_ts) as date,a.clicks
            from campaign_performance a
            join campaign_category_mapping b
            on (a.campaign_id = b.campaign_id )
            join category e on (e.id=b.category_id) 
            where e.category_type=''category'' ) zzz
     ORDER BY 1',''' + dstr1 + ''' as bfoo
        (rn int,
         product_category text,business_category text,
         ''' + dstr2 + ''' )
     cross join (select distinct order_channel from category_segment_actuals) c
     cross join (values ('new'),('existing')) bbb(customer_type)
    ) to '/tmp/clicks.csv' csv header;'''
print(basic + b2 + '\n')



#predictors
for pvar in pvars:
    basic = '''copy
    (select marketing_channel, tactic,customer_type,'none' as location,product_category, business_category,order_channel,''' + dstr0 + '''
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, product_category, business_category) AS rn,
                   marketing_channel, tactic,product_category, business_category,date, ''' + pvar
    b2 = ''' from
        (select platform_channel as marketing_channel,tactic_nm as tactic,product_category,business_category,event_ts as date,clicks,ad_spend 
        from
        ( select f.platform_channel,e.tactic_nm,d.category_type as product_category, d.category_nm as business_category,a.event_ts,sum(a.clicks) as clicks,sum(a.ad_spend) as ad_spend
          from campaign_performance a
          join campaign b
          on (a.campaign_id = b.id)
          join campaign_category_mapping c
          on (a.campaign_id=c.campaign_id)
          join category d
          on (c.category_id=d.id)
          join tactic e
          on (c.tactic_id=e.id)
          join platform_channel f
          on (b.platform_channel_id=f.id)
          group by platform_channel,tactic_nm,product_category,business_category,event_ts
          order by platform_channel,tactic_nm,product_category,business_category,event_ts
          ) aaa ) yyy
    order by 1 
    ',''' + dstr1 + '''
            as bfoo
            (rn int,
             marketing_channel text, tactic text , product_category text, business_category text,
             ''' + dstr2 + '''
            )
        cross join (values ('new'),('existing')) bbb(customer_type)
        cross join (select distinct order_channel from category_segment_actuals) ccc                
    )
    to '/tmp/p_''' + pvar + '''.csv' csv header;'''

    print(basic + b2 + '\n')
    #existing,none,category,Charms,offline,
    #existing, none, category, Necklaces & Pendants, offline,

    #marketing calendar.
    #(3 values .. global, specific category, or none).