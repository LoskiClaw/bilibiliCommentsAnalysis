USE mydb;
CREATE  TABLE IF NOT EXISTS bilicomment(
uname string,
sign string,
sex string,
mid int,
current_level string,
ctime string,
message string,
plat int,
likehah int,
rcount int
)
partitioned by (dt string)
row format delimited fields terminated by '\t';

create table IF NOT EXISTS biliusrinfo(
mid int,
name string,
sex string,
brank int,
face string,
birthday string,
sign string,
level int,
vipType int,
vipStatus int,
coins int,
userFollowing int,
userFans int
)
partitioned by (dt string)
row format delimited fields terminated by '\t';

create table if not exists comment_list(
comtime string,
content string)
partitioned by (dt string)
row format delimited fields terminated by '\t';

 create table if not exists usr_rank_list(
usr_rank int,
usrname string,
usrlevel int,
usrsex string,
usrlikes int)
partitioned by (dt string)
row format delimited fields terminated by '\t';

create table if not exists day_count_list(
daytime string,
countnum int
)
partitioned by (dt string)
row format delimited fields terminated by '\t';


