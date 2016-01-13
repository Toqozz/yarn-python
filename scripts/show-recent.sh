#! /bin/bash

pid=`cat /tmp/yarn-log | tail -1 | awk -F':' '{ print $1 }'`
summary=`cat /tmp/yarn-log | tail -1 | awk -F':' '{ print $2 }'`
body=`cat /tmp/yarn-log | tail -1 | awk -F':' '{ print $3 }'`

sed -i.bak "/$pid/d" /tmp/yarn-log

notify-send "$summary" "$body" -t 5
