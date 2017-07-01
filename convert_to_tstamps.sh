#!/bin/sh

# e.g., lineage_edges_20000.csv with cosmos events
file=$1

perl -pi -e 's/\t/,/g' $file
perl -pi -e 's/Input/read/g' $file
perl -pi -e 's/Output/write/g' $file

cat $file | cut -d, -f1-3 > $file.first_columns

echo "StartTime" > $file.fourth_column
cat $file | cut -d, -f4 | xargs -I {} date -j -f "%m/%d/%Y %I:%M:%S %p" "+%s000" {} >> $file.fourth_column

echo "EndTime" > $file.fifth_column
cat $file | cut -d, -f5 | xargs -I {} date -j -f "%m/%d/%Y %I:%M:%S %p%n" "+%s00" {} >> $file.fifth_column

paste -d',' $file.first_columns $file.fourth_column $file.fifth_column > $file.with_tstamps.csv

echo "Remember to mv $file.with_stamps.csv file to $file if it checks out."
