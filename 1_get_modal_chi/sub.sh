#!/bin/bash

for i in $(seq -f "%02g" 1 12)
do
  qsub $i.sub
  echo $i
done


