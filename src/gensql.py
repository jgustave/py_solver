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



#TODO: clicks as rvars


#
# select customer_type,'none' as location,product_category,business_category,order_channel,"_2019-10-19","_2019-10-20" from
# crosstab( 'select rank() OVER (ORDER BY product_category,business_category) as rn,
# 		   product_category,business_category,date,c_orders
# 		FROM
# 		 (select b.category_type as product_category,b.category_nm as business_category,a.date,a.c_orders,a.c_revenue from
# 			( select date(event_ts) as date, category_id, sum(orders) as c_orders, sum(revenue) as c_revenue from category_segment_actuals group by 1,2 ) a
# 			join
# 			category b on (a.category_id = b.id)) aaa
# 		 ORDER BY 1'
# 		 ,$$VALUES ('2019-10-19'),('2019-10-20')$$ )
# 		as bfoo
#             (rn int,
#              product_category text,business_category text,
#              "_2019-10-19" float,"_2019-10-20" float
#             )
# cross join (select distinct order_channel from category_segment_actuals) c
# cross join (values ('new'),('existing')) bbb(customer_type)



for rvar in rvars:

    basic = '''copy (select customer_type,'none' as location,product_category,business_category,order_channel,''' + dstr0 + ''' 
    from crosstab( 'select rank() OVER (ORDER BY product_category,business_category) as rn,
		   product_category,business_category,date, ''' + rvar

    b2 = ''' FROM 
		 (select b.category_type as product_category,b.category_nm as business_category,a.date,a.conversions,a.revenue from 
			( select date(event_ts) as date, category_id, sum(orders) as conversions, sum(revenue) as revenue from category_segment_actuals group by 1,2 ) a
			join
			category b on (a.category_id = b.id)) aaa
		 ORDER BY 1',''' + dstr1 + ''' as bfoo
            (rn int,
             product_category text,business_category text,
             ''' + dstr2 + ''' )
         cross join (select distinct order_channel from category_segment_actuals) c
         cross join (values ('new'),('existing')) bbb(customer_type)
        ) to '/tmp/''' + rvar + '''.csv' csv header;'''

    print(basic + b2 + '\n')

# select f.platform_channel,e.tactic_nm,d.category_type as product_category, d.category_nm as business_category,a.event_ts,a.clicks,a.ad_spend
# from campaign_performance a
# join campaign b
# on (a.campaign_id = b.id)
# join campaign_category_mapping c
# on (a.campaign_id=c.campaign_id)
# join category d
# on (c.category_id=d.id)
# join tactic e
# on (c.tactic_id=e.id)
# join platform_channel f
# on (b.platform_channel_id=f.id)


#Keep all dimensions
for pvar in pvars:

    basic = '''copy
    (select marketing_channel, tactic,customer_type,location,product_category, business_category,order_channel,''' + dstr0 + '''
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, customer_type,location,product_category, business_category,order_channel) AS rn,
                   marketing_channel, tactic, customer_type,location,product_category, business_category,order_channel, date, ''' + pvar
    b2 = ''' from
        (select platform_channel as marketing_channel,tactic_nm as tactic,customer_type,location,product_category,business_category,order_channel,event_ts as date,clicks,ad_spend 
        from
        (
        select *, ''none'' as location from (
        select f.platform_channel,e.tactic_nm,d.category_type as product_category, d.category_nm as business_category,a.event_ts,a.clicks,a.ad_spend
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
        where category_nm != ''All''
        order by b.platform_channel_id,tactic_nm,campaign_type,category_type,category_nm,event_ts
        ) aaa
        cross join (values (''new''),(''existing'')) bbb(customer_type)
        cross join (select distinct order_channel from category_segment_actuals) ccc
        ) ddd ) eee
    order by 1 
    ',''' + dstr1 + '''
            as bfoo
            (rn int,
             marketing_channel text, tactic text , customer_type text,location text,product_category text, business_category text,order_channel text,
             ''' + dstr2 + '''
            )
    )
    to '/tmp/p_''' + pvar + '''.csv' csv header;'''

    print(basic + b2 + '\n')


    #existing,none,category,Charms,offline,
    #existing, none, category, Necklaces & Pendants, offline,

    #marketing calendar.
    #(3 values .. global, specific category, or none).