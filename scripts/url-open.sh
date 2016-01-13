#!/bin/bash
# This script does not work currently.

#Get the latest notification displayed and negate the loopback_distance option.
var=`cat /tmp/dthread-log | tail -1 | awk -F'         ' '{ print $1 }'` #Split the strings if they have been looped, only use the first one.
#When something starts with 'http', send it to a new line.  After this, remove text after the end of the word/url.
link=`echo $var | grep http | sed 's/http/\nhttp/g' | grep ^http | sed 's/\(^http[^ <]*\)\(.*\)/\1/g'`
chromium $link      #Open chromium with the links

#For a one-liner:
#chromium $(cat /tmp/dthread-log | tail -1 | awk -F'         ' '{ print $1 }' | grep http | sed 's/http/\nhttp/g' | grep ^http | sed 's/\(^http[^ <]*\)\(.*\)/\1/g')
