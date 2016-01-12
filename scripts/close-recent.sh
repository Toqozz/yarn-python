#! /bin/bash

pid=`cat /tmp/dthread-log | tail -1 | awk -F':' '{ print $1 }'`
sed -i.bak "/$pid/d" /tmp/dthread-log
kill $pid


