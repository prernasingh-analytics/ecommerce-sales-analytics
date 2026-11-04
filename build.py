import pandas as pd, zipfile, json, pathlib, shutil
from plotly.offline import get_plotlyjs
root=pathlib.Path(__file__).resolve().parent; source_zip=root/'archive.zip'
if not source_zip.exists():
 raise SystemExit('Place the Kaggle dataset ZIP next to build.py and name it archive.zip')
z=zipfile.ZipFile(source_zip)
def load(n, cols=None):
 with z.open('olist_'+n+'_dataset.csv') as f:return pd.read_csv(f,usecols=cols)
orders=load('orders',['order_id','customer_id','order_status','order_purchase_timestamp'])
items=load('order_items',['order_id','price','product_id'])
customers=load('customers',['customer_id','customer_state','customer_unique_id'])
products=load('products',['product_id','product_category_name'])
with z.open('product_category_name_translation.csv') as f:trans=pd.read_csv(f)
orders['month']=orders.order_purchase_timestamp.str.slice(0,7)
d=orders.loc[orders.order_status.eq('delivered'),['order_id','customer_id','month']]
fact=items.merge(d,on='order_id',how='inner',validate='many_to_one').merge(customers,on='customer_id',validate='many_to_one').merge(products,on='product_id',how='left',validate='many_to_one').merge(trans,on='product_category_name',how='left',validate='many_to_one')
fact['category']=fact.product_category_name_english.fillna(fact.product_category_name).fillna('Unknown')
fact['state']=fact.customer_state.fillna('Unknown')
assert len(orders)==99441 and len(d)==96478 and len(fact)==110197
assert abs(fact.price.sum()-13221498.11)<0.1
agg=fact.groupby(['month','state','category'],as_index=False).agg(revenue=('price','sum'),items=('price','size'),orders=('order_id','nunique'))
agg.to_csv(root/'data'/'monthly_state_category.csv',index=False)
# order count across group is non-additive; for dashboard distinct order KPI use order-level month/state counts
oc=d.merge(customers,on='customer_id',validate='many_to_one').groupby(['month','customer_state']).size().reset_index(name='orders')
oc.rename(columns={'customer_state':'state'},inplace=True);oc.to_csv(root/'data'/'monthly_state_orders.csv',index=False)
metrics={'total_orders':len(orders),'delivered_orders':len(d),'delivered_items':len(fact),'delivered_item_revenue_brl':round(float(fact.price.sum()),2),'top_category':fact.groupby('category').price.sum().idxmax(),'time_period':'2016-09 to 2018-08'}
(root/'outputs'/'metrics.json').write_text(json.dumps(metrics,indent=2))
records=agg.round({'revenue':2}).to_dict('records'); counts=oc.to_dict('records')
# Customer-level analytics: one row per delivered order, avoiding item-join duplication.
order_values=items.groupby('order_id',as_index=False).agg(order_value=('price','sum'))
customer_orders=orders.loc[orders.order_status.eq('delivered'),['order_id','customer_id','order_purchase_timestamp']].merge(
    customers[['customer_id','customer_unique_id']],on='customer_id',validate='many_to_one').merge(
    order_values,on='order_id',validate='one_to_one')
customer_orders['order_purchase_timestamp']=pd.to_datetime(customer_orders['order_purchase_timestamp'])
snapshot=customer_orders.order_purchase_timestamp.max()+pd.Timedelta(days=1)
rfm=customer_orders.groupby('customer_unique_id').agg(
    last_purchase=('order_purchase_timestamp','max'),
    frequency=('order_id','nunique'),monetary=('order_value','sum'))
rfm['recency']=(snapshot-rfm.last_purchase).dt.days
rfm['segment']='Older one-time buyers'
rfm.loc[(rfm.frequency==1)&(rfm.recency<=90),'segment']='Recent one-time buyers'
rfm.loc[(rfm.frequency>=2)&(rfm.recency>90),'segment']='Other repeat buyers'
rfm.loc[(rfm.frequency>=2)&(rfm.recency<=90),'segment']='Recent repeat buyers'
segment_order=['Older one-time buyers','Recent one-time buyers','Other repeat buyers','Recent repeat buyers']
segment_summary=rfm.groupby('segment').agg(customers=('frequency','size'),revenue_brl=('monetary','sum')).reindex(segment_order,fill_value=0)
segment_summary['customer_pct']=100*segment_summary.customers/len(rfm)
segment_summary['revenue_pct']=100*segment_summary.revenue_brl/rfm.monetary.sum()
frequency_summary=rfm.frequency.value_counts().sort_index()
customer_metrics={
    'unique_customers':int(len(rfm)),
    'one_time_customers':int((rfm.frequency==1).sum()),
    'repeat_customers':int((rfm.frequency>=2).sum()),
    'repeat_rate_pct':round(float((rfm.frequency>=2).mean()*100),2),
    'average_order_value_brl':round(float(customer_orders.order_value.mean()),2),
    'median_order_value_brl':round(float(customer_orders.order_value.median()),2),
    'snapshot_date':str(snapshot.date()),
    'frequency_distribution':[{'orders':int(k),'customers':int(v)} for k,v in frequency_summary.items()],
    'segments':[{'name':str(k),'customers':int(row.customers),'revenue_brl':round(float(row.revenue_brl),2),
                 'customer_pct':round(float(row.customer_pct),2),'revenue_pct':round(float(row.revenue_pct),2)}
                for k,row in segment_summary.iterrows()]
}
(root/'outputs'/'customer_metrics.json').write_text(json.dumps(customer_metrics,indent=2))
segment_summary.round(2).to_csv(root/'outputs'/'customer_segments.csv',index_label='segment')

# embed JS and plotly offline
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Olist | E-Commerce Analytics</title><style>
:root{font-family:Inter,system-ui,-apple-system,sans-serif;color:#17253c;background:#f4f7fb}body{margin:0}.wrap{max-width:1220px;margin:auto;padding:32px 22px}h1{font-size:29px;margin:0 0 8px}p{color:#64748b;margin:0 0 22px}.filters{display:flex;gap:14px;flex-wrap:wrap;margin:24px 0}.filters label{font-weight:600;font-size:13px}select{display:block;margin-top:6px;min-width:190px;padding:11px;border:1px solid #d6e0eb;border-radius:9px;background:white}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.tile,.chart{background:white;border:1px solid #e3eaf2;border-radius:14px;box-shadow:0 2px 9px #17253c08}.tile{padding:20px}.tile small{color:#64748b}.tile strong{display:block;font-size:25px;margin-top:8px}.charts{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}.chart{padding:14px;min-width:0}.wide{grid-column:span 2}.foot{font-size:12px;line-height:1.7;margin-top:25px;color:#64748b}@media(max-width:780px){.kpis{grid-template-columns:repeat(2,1fr)}.charts{grid-template-columns:1fr}.wide{grid-column:span 1}}@media(max-width:460px){.kpis{grid-template-columns:1fr}}
.chart{height:390px;box-sizing:border-box;overflow:hidden;position:relative}.chart.wide{height:410px}.js-plotly-plot,.plot-container{max-width:100%}.customer-section{margin-top:42px;padding-top:12px;border-top:1px solid #dce5f0}.customer-section h2{font-size:24px;margin:18px 0 8px}.insights{background:white;border:1px solid #e3eaf2;border-radius:14px;padding:18px 22px;margin-top:18px}.insights h3{margin:0 0 10px}.insights p{line-height:1.65;margin:0 0 12px}
</style><script>'''+get_plotlyjs()+'''</script></head><body><main class="wrap"><h1>E-Commerce Sales & Customer Analytics</h1><p>Olist Brazilian E-Commerce Dataset · historical transactions (2016–2018) · delivered orders only</p><div class="filters"><label>Customer state<select id="state"></select></label><label>Product category<select id="category"></select></label></div><section class="kpis"><div class="tile"><small>Delivered item revenue</small><strong id="revenue"></strong></div><div class="tile"><small>Delivered items</small><strong id="items"></strong></div><div class="tile"><small>Orders represented in selected items*</small><strong id="orders"></strong></div><div class="tile"><small>Average item price</small><strong id="avg"></strong></div></section><section class="charts"><div class="chart wide" id="monthly"></div><div class="chart" id="categories"></div><div class="chart" id="states"></div></section><section class="customer-section"><h2>Customer Behaviour &amp; Segmentation</h2><p>Delivered orders only · customer identity based on customer_unique_id · snapshot CUSTOMER_SNAPSHOT</p><div class="kpis"><div class="tile"><small>Unique customers</small><strong id="uniqueCustomers"></strong></div><div class="tile"><small>Repeat customer rate</small><strong id="repeatRate"></strong></div><div class="tile"><small>Average order value</small><strong id="aov"></strong></div><div class="tile"><small>Median order value</small><strong id="medianAov"></strong></div></div><div class="charts"><div class="chart" id="frequencyChart"></div><div class="chart" id="segmentChart"></div><div class="chart wide" id="segmentRevenueChart"></div></div><div class="insights"><h3>Business interpretation</h3><p>Repeat purchasing is uncommon within the observed historical window. Investigate product replenishment cycles and customer cohorts before interpreting this as churn. Older one-time buyers account for most historical item revenue; segment-specific follow-up could be tested, not assumed effective.</p><p><strong>Method:</strong> Recency is days since last delivered-order purchase at the historical snapshot; frequency is distinct delivered orders; monetary is delivered item-price revenue, excluding freight. Recent means 90 days or less (an exploratory cutoff). Customer metrics are global and do not change with the sales filters above.</p></div></section><div class="foot">*Order count is the number of distinct orders represented by the selected item rows; it is calculated from the source data for the current state/category filter. Revenue is the sum of item prices, excluding freight, refunds, and payment adjustments; it is not profit. Purchase month is used. September 2016 and August 2018 are partial edge months. Data is historical and anonymized. No live company performance is implied.</div></main><script>
const rows=DATA_ROWS;const counts=ORDER_COUNTS;const allOrderCounts=FILTER_ORDER_COUNTS;const customerMetrics=CUSTOMER_METRICS;
const fmt=n=>new Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(n);const money=n=>'R$ '+new Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(n);
const s=document.getElementById('state'),c=document.getElementById('category');
function opts(el,vals){el.innerHTML='<option value="All">All</option>'+vals.map(v=>'<option>'+v+'</option>').join('')}
opts(s,[...new Set(rows.map(x=>x.state))].sort());opts(c,[...new Set(rows.map(x=>x.category))].sort());
function group(data,key){const out={};data.forEach(x=>out[x[key]]=(out[x[key]]||0)+x.revenue);return Object.entries(out).sort((a,b)=>b[1]-a[1])}
function draw(id,data,layout){const el=document.getElementById(id);const wide=el.classList.contains('wide');Plotly.react(el,data,{...layout,autosize:true,height:wide?365:345,paper_bgcolor:'white',plot_bgcolor:'white',font:{family:'Inter,system-ui',color:'#334155'},margin:{l:58,r:22,t:52,b:75,...(layout.margin||{})}}, {responsive:true,displaylogo:false})}
function update(){let st=s.value,cat=c.value;let f=rows.filter(x=>(st==='All'||x.state===st)&&(cat==='All'||x.category===cat));let rev=f.reduce((a,x)=>a+x.revenue,0),items=f.reduce((a,x)=>a+x.items,0);
let orderKey=st+'|'+cat;let orderCount=allOrderCounts[orderKey]||0;
document.getElementById('revenue').textContent=money(rev);document.getElementById('items').textContent=fmt(items);document.getElementById('orders').textContent=fmt(orderCount);document.getElementById('avg').textContent=money(items?rev/items:0);
let monthly=group(f,'month').sort((a,b)=>a[0].localeCompare(b[0]));draw('monthly',[{x:monthly.map(x=>x[0]),y:monthly.map(x=>x[1]),type:'scatter',mode:'lines+markers',line:{color:'#2563eb',width:3},fill:'tozeroy',fillcolor:'rgba(37,99,235,.08)',hovertemplate:'%{x}<br>R$ %{y:,.0f}<extra></extra>'}],{title:{text:'Monthly item revenue',x:.04,font:{size:17}},xaxis:{tickangle:-45},yaxis:{title:'BRL'}});
let cats=group(f,'category').slice(0,10).reverse();draw('categories',[{x:cats.map(x=>x[1]),y:cats.map(x=>x[0]),type:'bar',orientation:'h',marker:{color:'#0d9488'},hovertemplate:'%{y}<br>R$ %{x:,.0f}<extra></extra>'}],{title:{text:'Top 10 product categories',x:.04,font:{size:17}},xaxis:{title:'BRL'},yaxis:{automargin:true},margin:{l:150,r:20,t:52,b:55}});
let states=group(f,'state').slice(0,10);draw('states',[{x:states.map(x=>x[0]),y:states.map(x=>x[1]),type:'bar',marker:{color:'#7c3aed'},hovertemplate:'%{x}<br>R$ %{y:,.0f}<extra></extra>'}],{title:{text:'Top 10 customer states',x:.04,font:{size:17}},xaxis:{title:'State'},yaxis:{title:'BRL'}})}
s.addEventListener('change',update);c.addEventListener('change',update);update();
// Customer analytics are intentionally independent of sales state/category filters.
document.getElementById('uniqueCustomers').textContent=fmt(customerMetrics.unique_customers);
document.getElementById('repeatRate').textContent=customerMetrics.repeat_rate_pct.toFixed(2)+'%';
document.getElementById('aov').textContent='R$ '+customerMetrics.average_order_value_brl.toFixed(2);
document.getElementById('medianAov').textContent='R$ '+customerMetrics.median_order_value_brl.toFixed(2);
const freq=customerMetrics.frequency_distribution;
draw('frequencyChart',[{x:freq.map(x=>String(x.orders)),y:freq.map(x=>x.customers),type:'bar',marker:{color:'#2563eb'},hovertemplate:'%{x} orders<br>%{y:,} customers<extra></extra>'}],{title:{text:'Delivered orders per customer',x:.04,font:{size:17}},xaxis:{title:'Number of orders'},yaxis:{title:'Customers',type:'log'}});
const seg=customerMetrics.segments;
draw('segmentChart',[{x:seg.map(x=>x.name),y:seg.map(x=>x.customer_pct),type:'bar',marker:{color:'#0d9488'},hovertemplate:'%{x}<br>%{y:.2f}% of customers<extra></extra>'}],{title:{text:'Customer segment share',x:.04,font:{size:17}},xaxis:{tickangle:-25},yaxis:{title:'Share of customers (%)'}});
draw('segmentRevenueChart',[{x:seg.map(x=>x.name),y:seg.map(x=>x.revenue_pct),type:'bar',marker:{color:'#7c3aed'},hovertemplate:'%{x}<br>%{y:.2f}% of item revenue<extra></extra>'}],{title:{text:'Item revenue contribution by customer segment',x:.04,font:{size:17}},xaxis:{tickangle:-15},yaxis:{title:'Share of item revenue (%)'}});
</script></body></html>'''
# distinct orders by state and category, from item rows; avoid double count from aggregate
order_counts={}
for st,cat,group in [('All','All',fact)]:pass
for (st,cat),g in fact.groupby(['state','category']):order_counts[st+'|'+cat]=int(g.order_id.nunique())
for st,g in fact.groupby('state'):order_counts[st+'|All']=int(g.order_id.nunique())
for cat,g in fact.groupby('category'):order_counts['All|'+cat]=int(g.order_id.nunique())
order_counts['All|All']=int(fact.order_id.nunique())
html=html.replace('CUSTOMER_METRICS',json.dumps(customer_metrics,separators=(',',':'))).replace('CUSTOMER_SNAPSHOT',customer_metrics['snapshot_date']).replace('FILTER_ORDER_COUNTS',json.dumps(order_counts,separators=(',',':'))).replace('DATA_ROWS',json.dumps(records,separators=(',',':'))).replace('ORDER_COUNTS',json.dumps(counts,separators=(',',':')))
(root/'dashboard'/'index.html').write_text(html)
(root/'sql'/'analysis.sql').write_text('''-- Import source CSVs as orders, order_items, products, customers, category_translation.\n-- This query excludes freight and limits to delivered orders.\nSELECT substr(o.order_purchase_timestamp,1,7) AS purchase_month,\n       ROUND(SUM(i.price),2) AS delivered_item_revenue_brl,\n       COUNT(DISTINCT o.order_id) AS orders, COUNT(*) AS items\nFROM orders o JOIN order_items i ON o.order_id=i.order_id\nWHERE o.order_status='delivered'\nGROUP BY 1 ORDER BY 1;\n\nSELECT COALESCE(t.product_category_name_english,p.product_category_name,'Unknown') AS category,\n       ROUND(SUM(i.price),2) AS item_revenue_brl\nFROM orders o JOIN order_items i ON o.order_id=i.order_id\nLEFT JOIN products p ON p.product_id=i.product_id\nLEFT JOIN category_translation t ON t.product_category_name=p.product_category_name\nWHERE o.order_status='delivered' GROUP BY 1 ORDER BY 2 DESC LIMIT 10;\n''')

(root/'requirements.txt').write_text('pandas>=2.0,<3\nplotly>=5.0,<7\n')
(root/'.gitignore').write_text('__pycache__/\n.DS_Store\n*.zip\n.env\n')
(root/'LICENSE').write_text('MIT License\n\nCopyright (c) 2026 Portfolio project contributor\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.\n')
# Keep the repository README.md unchanged when regenerating analysis outputs.

print(metrics,'dashboard bytes',len(html),'aggregate rows',len(agg))
