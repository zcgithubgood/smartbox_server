#! /bin/sh
host_dir=`echo ~`                                       # 当前用户根目录
#proc_name="runserver"                                  # 进程名
proc_name="uwsgi"                                  # 进程名
file_name="/home/ubuntu/temp/server_debug.log"           # 日志文件
proc_id()                                               # 计算进程数
{	
	pid=`ps -ef | grep $proc_name | grep -v grep | awk '{print $2}'`
	kill -9 $pid;
}

proc_id
proId=$?

echo "proc_id:$proId ?= $pid"

if [ $pid -eq 0 ] 
then	
	cd $host_dir/gitsmartbox/smartbox-server/
	kill -9 $pid;	
	#nohup ./switch_pro &> ../test/test.txt &	
	echo ${pid}, `date` >> $file_name          # 将新进程号和重启时间记录
fi

