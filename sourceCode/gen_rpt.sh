#!\bin\bash
d = $(date +%y%m%d)
hive -e "use mydb;insert overwrite table comment_list partition (dt=${d})
select 
ctime as comtime,
message as content 
from bilicomment 
where dt=${d}
order by comtime desc;"