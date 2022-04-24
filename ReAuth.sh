pid=$(ps -ef | grep "python -u main.py YCalarm" | grep -v grep | head -1 | awk '{ print $2 }')
if [ -n $pid ]
then
    kill -s SIGUSR1 $pid
    echo "Signal sent."
    sleep 5s
    tail -100 logs/latest.log | grep "Auth URL"
    echo "Enter code : "
    read code
    echo $code > AuthCode.txt
else
    echo "Process is not running."
fi
