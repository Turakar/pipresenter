#!/bin/bash

pipe=/tmp/keyboarder

# Delete pipe on exit
trap "rm -f $pipe" EXIT

rm -f $pipe
mkfifo $pipe

# Wait for input
while true
do
  read -t 10 line <> $pipe
  if [ $? == 0 ]; then
    # Press Key
    xdotool key $line
    # Quit on Escape
    if [[ "$line" == 'Escape' ]]; then
      break
    fi
  fi
  xdotool key Ctrl
done
