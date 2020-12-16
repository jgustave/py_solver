


--CREATE EXTENSION IF NOT EXISTS tablefunc;

select *
from crosstab('select rank() OVER (ORDER BY platform_channel, tactic, campaign, product_category, business_category) AS rn,
			   platform_channel, tactic, campaign, product_category, business_category, date, spend from bigfoo
			   order by 1',
			   $$VALUES ('2020-12-02'), ('2020-12-03'), ('2020-12-04'),('2020-12-05'), ('2020-12-06'), ('2020-12-07')$$ )
					as bfoo
					(rn int,
					 platform_channel text, tactic text, campaign text, product_cateogory text, business_category text,
					 "2020-12-02" float,
					 "2020-12-03" float,
					 "2020-12-04" float,
					 "2020-12-05" float,
					 "2020-12-06" float,
					 "2020-12-07" float
					);




select f.platform_channel,e.tactic_nm,b.campaign_nm,b.campaign_type,d.category_type, d.category_nm,a.event_ts,a.clicks,a.conversions,a.revenue
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
where event_ts > '2020-12-01' and category_nm != 'All'
order by b.platform_channel_id,tactic_nm,campaign_nm,campaign_type,category_type,category_nm,event_ts



