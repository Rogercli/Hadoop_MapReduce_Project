#!/usr/bin/python
# if testing locally, use !#/path/to/local/python
import sys

# [Define group level master information]
vin_dict={}
master_vin=None
vin=None
make=None
year=None
incident_list=[]
accident_count=0


def reset():
    global master_vin
    global make
    global year
    global accident_count
    master_vin = None
    make = None
    year = None
    accident_count=0



def flush():
    global master_vin
    global make
    global accident_count
    global year
    type='A'
    for _ in range(accident_count):
            print('%s\t%s' % (master_vin,(type,make,year)))
for line in sys.stdin:

    newline=line.strip()
    newline=line.split("\t")
# [parse the input we got from mapper and update the master info]
    current_vin=newline[0]
    value=eval(newline[1])
    if current_vin != master_vin:
        #Write result to stdout
        if current_vin != None:
            flush()
        reset()
    if value[0]=='I': 
            make=value[1]
            year=value[2]
    # update more master info after the key change handling
    if value[0]=='A':
        accident_count+=1
    master_vin = current_vin
    

# # do not forget to output the last group if needed!
flush()
