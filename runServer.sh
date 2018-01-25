#! /bin/sh

host_dir=`echo ~`                                       # 当前用户根目录
proc_name="runserver"                                  # 进程名
#file_name="/home/ubuntu/temp/server_debug.log"           # 日志文件
file_name="/home/ubuntu/gitsmartbox/smartbox-server/server_debug.log"           # 日志文件
pid=0

Epython="/home/ubuntu/chunyu/ENV_smartbox/bin/python"
Euwsgi="/home/ubuntu/chunyu/ENV_smartbox/bin/uwsgi"

proc_num()                                              # 计算进程数
{
        num=`ps -ef | grep $proc_name | grep -v grep | wc -l`
        #echo $num
        return $num
}

proc_id()                                               # 进程号
{
        pid=`ps -ef | grep $proc_name | grep -v grep | awk '{print $2}'`
}

proc_num
number=$?

echo "proc_num:$number ?= $num"

if [ $number -eq 0 ]                                    # 判断进程是否存在
then
        echo "here"
        #cd $host_dir/temp/smartbox/
        cd $host_dir/gitsmartbox/smartbox-server/
        #(./switch_pro &> ../../test.txt &)                 # 重启进程的命令，请相应修改
        #nohup $Epython manage.py runserver 0.0.0.0:8000 &> ../test/test.txt &
        nohup $Euwsgi --socket :9000 --master-fifo /tmp/fifo0 --wsgi-file ./wsgi.py --chmod-socket=664 --processes 64 &> ../test/test.txt &
        proc_id                                             # 获取新进程号
        echo ${pid}, `date` >> $file_name          # 将新进程号和重启时间记录
fi
