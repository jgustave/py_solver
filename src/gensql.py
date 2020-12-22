from datetime import timedelta, date

#Code generate some SQL.

#Start and end dates
start_date = date(2020, 10, 19)
end_date = date(2020, 10, 30)


delta = timedelta(days=1)
dl = []

while start_date <= end_date:
    dl.append( start_date )
    start_date += delta
    #start_date.strftime("%Y-%m-%d")

#Make date range strings
dstr1 = '$$VALUES '
for d in dl:
    dstr1 += ("('" + d.strftime("%Y-%m-%d") + "'),")
dstr1 = dstr1[0:-1] + '$$ )'

dstr2 = ''
for d in dl:
    dstr2 += ('"' + d.strftime("%Y-%m-%d") + '" float,')
dstr2 = dstr2[0:-1]


pvars = ['ad_spend','conversions','clicks','revenue']

for pvar in pvars:

    basic = '''copy
    (select *
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel) AS rn,
                   marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel, date, ''' + pvar
    b2 = ''' from
        (select platform_channel as marketing_channel,tactic_nm as tactic,campaign_nm as campaign,customer_type,location,product_category,business_category,order_channel,event_ts as date,clicks,conversions,revenue,ad_spend 
        from
        (
        select *, ''none'' as location from (
        select f.platform_channel,e.tactic_nm,b.campaign_nm,d.category_type as product_category, d.category_nm as business_category,a.event_ts,a.clicks,g.c_orders as conversions,g.c_revenue as revenue,a.ad_spend
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
		left join (select date(event_ts) as c_date,category_id, sum(orders) as c_orders, sum(revenue) as c_revenue from category_segment_actuals group by 1,2) g
	    on(c.category_id = g.category_id and a.event_ts = g.c_date)        
        where category_nm != ''All''
        order by b.platform_channel_id,tactic_nm,campaign_nm,campaign_type,category_type,category_nm,event_ts
        ) aaa
        cross join (values (''new''),(''existing'')) bbb(customer_type)
        cross join (select distinct order_channel from category_segment_actuals) ccc
        ) ddd ) eee
    order by 1 
    ',''' + dstr1 + '''
            as bfoo
            (rn int,
             marketing_channel text, tactic text , campaign text, customer_type text,location text,product_category text, business_category text,order_channel text,
             ''' + dstr2 + '''
            )
    )
    to '/tmp/''' + pvar + '''.csv' csv header;'''

    print(basic + b2 + '\n')
