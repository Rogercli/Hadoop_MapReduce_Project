#!/usr/bin/python
# if testing locally, use !#/path/to/local/python
import sys
total_dict={}
for line in sys.stdin:
    newline=line.split('\t')
    model_year,count=newline[0],int(newline[1])
    if model_year in total_dict.keys():
        total_dict[model_year]+=1
    else:
        total_dict[model_year]=1

for make_year,count in total_dict.items():
    print('%s\t%s' % (make_year,count))
