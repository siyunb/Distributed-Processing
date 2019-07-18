use cufe_wangsiyu1;
insert overwrite local directory '/home/lifeng/pc2017fall/cufe_wangsiyu/lab3/result' 
select AVG(price_close),AVG(price_open),AVG(price_high),AVG(price_low), exchanges
from stocks
where symbol = 'AAPL'
group by exchanges;
