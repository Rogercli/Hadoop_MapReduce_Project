#!/usr/bin/python
# if testing locally, use !#/path/to/local/python
import sys
# input comes from STDIN (standard input)
for line in sys.stdin:
# derive mapper output key values
    newline=line.split('\t')
    value=eval(newline[1])
    make,year=value[1],value[2]
    count=1
    print('%s\t%s' % (make+year,count))
