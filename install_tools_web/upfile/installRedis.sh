#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/opt/bin:~/bin
export PATH

if [ $(id -u) != "0" ];then
    echo "请用root用户登入运行安装"
    exit 1
fi

NET_NUM=`ping -c 4 www.baidu.com |awk '/packet loss/{print $6}' |sed -e 's/%//'`
if [ -z "$NET_NUM" ] || [ $NET_NUM -ne 0 ];then
    echo "请修改您的网络设置"
    exit 1
fi

if [ -s redis-5.0.9.tar.gz ];then
#    echo -e "\033[40;31m redis-5.0.tar.gz [found]\-33[40;37m"
     echo "redis-5.0.9.tar.gz 已存在"
else
    wget http://download.redis.io/releases/redis-5.0.9.tar.gz
fi

# yum -y install gcc gcc-c++ make
user_redis=`cat /etc/passwd|grep redis|awk -F : '{print $1}'`
if [ -z "$user_redis" ];then
    useradd -s /bin/bash -M redis
else
    echo "redis已经存在,不需要重复安装"
    exit 0
fi

redis_port=6379

mkdir -p /data/redis/member-$redis_port/{conf,data,log,pid}
tar zxf redis-5.0.9.tar.gz -C /usr/local
mv /usr/local/redis-5.0.9 /usr/local/redis
cd /usr/local/redis
make && make install

cp /usr/local/redis/redis.conf /data/redis/member-$redis_port/conf/
chown -R redis.redis /data/redis/member-$redis_port
cat >/data/redis/member-$redis_port/conf/redis.conf <<EOF
daemonize yes
pidfile /data/redis/memeber-$redis_port/pid/redis.pid
port $redis_port
tcp-backlog 65535
bind 127.0.0.1
timeout 0
tcp-keepalive 0
loglevel notice
logfile /data/redis/memeber-$redis_port/log/redis.log
databases 16
lua-time-limit 5000
maxclients 10000
dir /data/redis/member-$redis_port/data

slowlog-log-slower-than 10000
slowlog-max-len 128

maxmemory 2G
maxmemory-policy volatile-lru

save 3600 1
stop-writes-on-basave-error no
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb

no-appendfsync-on-rewrite yes
appendonly yes
appendfilename "appendonly.aof"
appendfsync no
auto-aof-rewrite-min-size 512mb
auto-aof-rewrite-percentage 100
aof-load-truncated yes
aof-rewrite-incremental-fsync yes

client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-entries 512
list-max-ziplist-value 64
set-max-intset-entries 512
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
latency-monitor-threshold 0
hz 10
EOF

echo 'export PATH=$PATH:/usr/local/bin' >>/etc/profile

source /etc/profile

# sudo -u redis 'which reids-server'
# /data/redis/member-$redis_port/conf/redis.conf

echo "redis5.0.9安装完成"
