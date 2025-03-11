#!\bin\bash
set -x
d=$(date +%y%m%d)
hive -e "load data inpath 'hdfs://hadoop1:9000/user/loski/bilicomment/part-m-00000' into table mydb.bilicomment partition(dt=${d});"
hadoop fs -rm -r /user/loski/bilicomment
hive -e "load data inpath 'hdfs://hadoop1:9000/user/loski/biliusrinfo/part-m-00000' into table mydb.biliusrinfo partition(dt=${d});"
hadoop fs -rm -r /user/loski/biliusrinfo
hive -e "load data inpath 'hdfs://hadoop1:9000/user/loski/usr_rank_list/part-m-00000' into table mydb.usr_rank_list partition(dt=${d});"
hadoop fs -rm -r /user/loski/usr_rank_list
hive -e "load data inpath 'hdfs://hadoop1:9000/user/loski/day_count_list/part-m-00000' into table mydb.day_count_list partition(dt=${d});"
hadoop fs -rm -r /user/loski/day_count_list
