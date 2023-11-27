#!/bin/bash

python3 src/main.py > out/own_solution.out
python3 src/accuracy.py out/own_solution.out out/solution.out
