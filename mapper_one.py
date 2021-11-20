#!/usr/bin/python
# if testing locally, use !#/path/to/local/python
import sys
# input comes from STDIN (standard input)
for line in sys.stdin:
# derive mapper output key values
    newline=line.split(',')
    incident_type,make,year=newline[1],newline[3],newline[5]
    vin=newline[2]
    print('%s\t%s' % (vin,(incident_type,make,year)))
