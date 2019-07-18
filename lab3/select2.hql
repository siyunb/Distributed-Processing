 
use cufe_wangsiyu1;
insert overwrite local directory '/home/lifeng/pc2017fall/cufe_wangsiyu/lab3/result2'
select AVG(price_close),AVG(price_open),SUM(volume),symbol
from stocks
where exchanges='NASDAQ'
group by symbol
order by symbol;

