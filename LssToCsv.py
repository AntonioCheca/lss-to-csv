import argparse
from lxml import etree
import csv
import re

# Changes hh:mm:ss.abcdefg format to just number of ms
def timeToNumberOfMicroSeconds(s):
    l = list(map(lambda x: int(x), re.split('[.:]', s)))
    while(len(l) < 4):
        l.append(0)
    while(l[3] > 1000):
        l[3] = l[3]/10
    return (l[0]*3600+l[1]*60+l[2])*1000+l[3]

def getTransformationOfTime(s, option):
    if(option == 'ms'):
        return timeToNumberOfMicroSeconds(s)
    else:
        return s

parser = argparse.ArgumentParser(description='Get times from your lss file to csv.')
parser.add_argument('input', metavar='input filename', type=str, nargs=None,
                    help='input lss file name')
parser.add_argument('output', metavar='output filename', type=str, nargs=None,
                    help='output csv file name')
parser.add_argument('-time', type=str, nargs=None, help='how to output time, ms will output in milliseconds, anything else will let the time as it is')

args = parser.parse_args()
args=vars(args)
input = args["input"]
output = args["output"]
option=args['time']

attemptHistory = 'AttemptHistory'
segments = 'Segments'
segmentHistory = 'SegmentHistory'

lssFile = etree.fromstring(etree.tostring(etree.parse(input)))

timesList = {}
headers = ['Id of run', 'Timing method', 'Full run time']
timesList[0] = headers
id = 1
for node in lssFile:
    if(attemptHistory == node.tag):
        id = 1
        for attempt in node:
            if(len(attempt) > 1):
                timesList[id] = [id, attempt[1].tag, getTransformationOfTime(attempt[1].text, option)]
            elif(len(attempt) == 1):
                timesList[id] = [id, attempt[0].tag, getTransformationOfTime(attempt[0].text, option)]
            id = id+1
    elif(segments == node.tag):
        for segment in node:
            headers.append(segment[0].text)
            for segmentNode in segment:
                if(segmentHistory == segmentNode.tag):
                    for record in segmentNode:
                        idOfRun = int(record.values()[0])
                        if(len(record) > 0):
                            lastTime = record[-1].text
                            if(idOfRun in timesList.keys()):
                                timesList[idOfRun].append(getTransformationOfTime(lastTime, option))
                            else:
                                timesList[idOfRun] = [idOfRun, record[-1].tag, 'NotFullRun', getTransformationOfTime(lastTime, option)]


with open(output, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for t in sorted(timesList.keys()):
        writer.writerow(timesList[t])
