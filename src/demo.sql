
CREATE EXTENSION IF NOT EXISTS tablefunc;

copy
    (select *
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel) AS rn,
                   marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel, date, ad_spend from
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
    ',$$VALUES ('2020-12-01'),('2020-12-02'),('2020-12-03'),('2020-12-04'),('2020-12-05'),('2020-12-06'),('2020-12-07'),('2020-12-08')$$ )
            as bfoo
            (rn int,
             marketing_channel text, tactic text , campaign text, customer_type text,location text,product_category text, business_category text,order_channel text,
             "2020-12-01" float,"2020-12-02" float,"2020-12-03" float,"2020-12-04" float,"2020-12-05" float,"2020-12-06" float,"2020-12-07" float,"2020-12-08" float
            )
    )
    to '/tmp/ad_spend.csv' csv header;

copy
    (select *
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel) AS rn,
                   marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel, date, conversions from
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
    ',$$VALUES ('2020-12-01'),('2020-12-02'),('2020-12-03'),('2020-12-04'),('2020-12-05'),('2020-12-06'),('2020-12-07'),('2020-12-08')$$ )
            as bfoo
            (rn int,
             marketing_channel text, tactic text , campaign text, customer_type text,location text,product_category text, business_category text,order_channel text,
             "2020-12-01" float,"2020-12-02" float,"2020-12-03" float,"2020-12-04" float,"2020-12-05" float,"2020-12-06" float,"2020-12-07" float,"2020-12-08" float
            )
    )
    to '/tmp/conversions.csv' csv header;

copy
    (select *
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel) AS rn,
                   marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel, date, clicks from
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
    ',$$VALUES ('2020-12-01'),('2020-12-02'),('2020-12-03'),('2020-12-04'),('2020-12-05'),('2020-12-06'),('2020-12-07'),('2020-12-08')$$ )
            as bfoo
            (rn int,
             marketing_channel text, tactic text , campaign text, customer_type text,location text,product_category text, business_category text,order_channel text,
             "2020-12-01" float,"2020-12-02" float,"2020-12-03" float,"2020-12-04" float,"2020-12-05" float,"2020-12-06" float,"2020-12-07" float,"2020-12-08" float
            )
    )
    to '/tmp/clicks.csv' csv header;

copy
    (select *
    from crosstab('select rank() OVER (ORDER BY marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel) AS rn,
                   marketing_channel, tactic, campaign, customer_type,location,product_category, business_category,order_channel, date, revenue from
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
    ',$$VALUES ('2020-12-01'),('2020-12-02'),('2020-12-03'),('2020-12-04'),('2020-12-05'),('2020-12-06'),('2020-12-07'),('2020-12-08')$$ )
            as bfoo
            (rn int,
             marketing_channel text, tactic text , campaign text, customer_type text,location text,product_category text, business_category text,order_channel text,
             "2020-12-01" float,"2020-12-02" float,"2020-12-03" float,"2020-12-04" float,"2020-12-05" float,"2020-12-06" float,"2020-12-07" float,"2020-12-08" float
            )
    )
    to '/tmp/revenue.csv' csv header;

