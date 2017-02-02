#!/bin/sh

in1=in1.csv
in2=in2.csv
out1=out1.csv

echo "Copying a file via UNIX cp:"
echo "cp $in1 $out1"
cp $in1 $out1
sleep 1

echo ""
echo "Copying a file via UNIX cat:"
echo "cat $in1 > $out1"
cat $in1 > $out1
sleep 1

echo ""
echo "Copying multiple files into a single one via python script:"
echo "python concat_csvs.py $in1 $in2"
python concat_csvs.py $in1 $in2
sleep 1

