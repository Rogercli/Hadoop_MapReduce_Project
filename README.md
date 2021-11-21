

# Hadoop MapReduce Project
## Overview
  In this project, my goal was to write a MapReduce program to produce a report of the total number of accidents per make and
year of the car. I utilized data from an automobile tracking platform that tracks the history of
important incidents after the initial sale of a new vehicle. The solution was written in Python to create MapReduce jobs and the program was run in a Hortonwork HDP Sandbox on top of Docker.

## Summary of files
- **Data.csv**: Input file of car incidents of different types ("R"= Repair, "I"= Initial Sale, "A"=Accident). Information regarding car make and year is null in Type A and Type I rows 
- **mapper_one.py**: First mapper parses for columns of interest and creates a key/value pair with VIN number as the aggregate key(key=VIN, value=(incident_type, make, year))
- **reducer_one.py**: First reducer propagates the make and year from the Type I to Type A incidents, and reduces down to only Type A incidents 
- **mapper_two.py**: Second mapper reads the Type A input, and creates a composite key of make and value of 1 (key=make+year,value=1)
- **reducer_two.py**: Second reducer groups by composite key and sums the values to reduce down to a composite key with total count
- **run_script.sh**: Shell script using Hadoop streaming libary to call MapReduce code and run in a distributed mode
- **HDFS_accident_type_output.png**: Image of path to output/Accident_type on HDFS which is result of first MapReduce jobs
- **HDFS_accident_count_output.png**: Image of path to output/Accident_count on HDFS which is result of second and final MapReduce jobs

## Testing Locally
- **Dependencies**: Ensure that the MapReduce and Shell files are executable. In addition, ensure you have the appropriate hashbang at the top of each file !#/local/path/to/python
- **Testing first MapReduce**

```cat data.csv | ./mapper_one.py | sort | ./reducer_one.py```
```
EXOA00341AB123456	('A', 'Mercedes', '2016')
INU45KIOOPA343980	('A', 'Mercedes', '2015')
VOME254OOXW344325	('A', 'Mercedes', '2015')
VXIO456XLBB630221	('A', 'Nissan', '2003')
```

- **Testing Second MapReduce**

``` cat data.csv | ./mapper_one.py | sort | ./reducer_one.py | sort | ./mapper_two.py | sort | ./reducer_two.py  | sort```
```
Mercedes2015	2
Mercedes2016	1
Nissan2003	1
```
## Running in HDP Sandbox on Docker
- **Dependencies**: Ensure that the MapReduce and Shell files are executable. In addition, ensure that the hashbang at the top of each file has been changed from the local path to sandbox path !#/sandbox/path/to/python 

- **Step 1**: Copy all files (data,MapReduce scripts,shell script) from local filesystem to Docker container. Note: Using docker cp does not persist the files in the container, once container is stopped all data is lost. To persist data, use mount or volumes in Docker.
```
docker cp /your/local/path/to/files sandbox-hdp:/home/hdfs
```
- **Step 2**: Once all files are in your container, enter the HDP Sandbox
```
docker exec -it sandbox-hdp bin/bash
```
- **Step 3**: Create input and output directory for HDFS 
```
hdfs dfs -mkdir input
hdfs dfs -mkdir ouput
```
- **Step 4**: Add cars data into HDFS input directory
```
hdfs dfs -put data.csv input
```
- **Step 5**: Run shell script 
``` 
sh run_script.sh
```

## Problems Encountered
- **Problem 1**: Docker Container "sandbox-proxy" would exit/crash immediately upon starting the container.
  - Error: nginx: [emerg] host not found in upstream "sandbox-hdp" in /etc/nginx/conf.d/http-hdp.conf:9
- **Problem 2**: Once inside Sandbox-HDP, unable to execute HDFS commands
  - Error: java.net.UnknownHostException: sandbox-hdp.hortonworks.com
- **Solution**: Both problem 1 and 2 were related to hostname issues as a result of incorrect deployment script from Cloudera. To resolve this, we need to edit the deployment script from Cloudera, remove HDP and Proxy Containers, and re-deploy them using the edited script (https://jae-huang111.medium.com/deploy-sandbox-hdp-via-docker-debug-note-b082b33db3e).
- **Problem 3**: Running the MapReduce files in HDP sandbox failed
  - Error: java.lang.RuntimeException: Error in configuring object
- **Solution**: Edit MapReduce shebang(!#) from local path to python to Sandbox path to python. While in the sandbox,use command "whereispython" to find path.
- **Problem 4**: Shell script failed when using Hadoop Streaming libary due to incorrect jar file 
  - Error: JAR does not exist or is not a normal file: /usr/hdp/3.0.1.0-187/hadoop-mapreduce/hadoop-streaming.jar-file
- **Solution**: Use command "find / -name *hadoop-streaming*.jar" to find correct jar file and update Shell script
