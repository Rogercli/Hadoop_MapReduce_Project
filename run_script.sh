#bin/bash

echo "Running mapreduce one"
hadoop jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming-3.1.1.3.0.1.0-187.jar \
-file mapper_one.py -mapper mapper_one.py \
-file reducer_one.py -reducer reducer_one.py \
-input input/data.csv -output output/accident_type

echo "Running mapreduce two"
hadoop jar /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming-3.1.1.3.0.1.0-187.jar \
-file mapper_two.py -mapper mapper_two.py \
-file reducer_two.py -reducer reducer_two.py \
-input output/accident_type -output output/accident_count


