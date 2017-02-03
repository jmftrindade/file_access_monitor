#!/bin/sh

run_copy_cmd() {
  local cmd="$1"
  local args="$2"

  echo "Copying files via $cmd:"
  echo "$cmd $args"
  eval $cmd $args
  sleep 1
  echo ""
}

run_copy_cmd "cp" "in1.csv out1.csv"
run_copy_cmd "cat" "in1.csv > out2.csv"
run_copy_cmd "python" "concat_csvs.py in1.csv in2.csv out2.csv out3.csv"
run_copy_cmd "cat" "out3.csv > out4.csv"
