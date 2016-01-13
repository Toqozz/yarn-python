#! /bin/bash

pid=`cat /tmp/yarn-log | tail -1 | awk -F':' '{ print $1 }'`
sed -i.bak "/$pid/d" /tmp/yarn-log
kill $pid


