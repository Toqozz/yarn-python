#! /bin/bash

pid=`cat /tmp/dthread-log | tail -1 | awk -F':' '{ print $1 }'`
summary=`cat /tmp/dthread-log | tail -1 | awk -F':' '{ print $2 }'`
body=`cat /tmp/dthread-log | tail -1 | awk -F':' '{ print $3 }'`

sed -i.bak "/$pid/d" /tmp/dthread-log

notify-send "$summary" "$body" -t 5
