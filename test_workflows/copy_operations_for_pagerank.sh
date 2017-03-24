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

run_copy_cmd "python" "concat_csvs.py in1.csv in2.csv in3.csv in4.csv out3.csv"
run_copy_cmd "python" "concat_csvs.py in1.csv in2.csv in3.csv in4.csv out4.csv"
run_copy_cmd "cp" "out3.csv out5.csv"
run_copy_cmd "cp" "out4.csv out6.csv"
run_copy_cmd "cp" "out5.csv out7.csv"
run_copy_cmd "cp" "out7.csv out9.csv"
