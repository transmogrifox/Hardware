#!/bin/bash
g++ expo_decay.c -o dcyexp
./dcyexp

head -n 5 data_expo.txt
echo "..."
head -n 500 data_expo.txt | tail -n 5
echo "..."
tail -n 117 data_expo.txt | head -n 5

python3 plot_data_expo.py &
