#!/bin/bash


for(( START = 0; START <= 10; START += 1 ))
do
    sbatch part1-same.sb
    sbatch part1-differ.sb
    sbatch part2-same.sb
    sbatch part2-differ.sb
done
