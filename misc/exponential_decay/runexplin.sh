#!/bin/bash
g++ expo_lin_decay.c -o dcyexplin
./dcyexplin

head -n 5 data_expo_lin.txt
echo "..."
head -n 500 data_expo_lin.txt | tail -n 5
echo "..."
tail -n 117 data_expo_lin.txt | head -n 5

python3 plot_data_expo_lin.py &
