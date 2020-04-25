#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
# Copyright (c) 2020 Dominik Tomaszuk (University of Bialystok)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.


import argparse
import xmltodict
import uuid
import os
import sys

def writeStdErr(message):
    sys.stderr.write(message)

if sys.version_info[0] < 3:
    writeStdErr('\nPython2 is not supported\n')
    exit()

parser = argparse.ArgumentParser(description='Converter')
parser.add_argument('file', type=str, help='a GraphML file')
args = parser.parse_args()

if args.file:
  with open(args.file, 'r') as content_file:
    try:
      content = content_file.read()
    except:
      exit()

all = xmltodict.parse(content, process_namespaces=False)

for x in range(len(all['graphml']['graph']['edge'])):
    edge_label = all['graphml']['graph']['edge'][x]['@id']
    edge_source = all['graphml']['graph']['edge'][x]['@source']
    edge_target = all['graphml']['graph']['edge'][x]['@target']
    print('(' + edge_source + ')-[]->(' + edge_target + ')')


for y in range(len(all['graphml']['graph']['node'])):
    node_label = all['graphml']['graph']['node'][y]['@id']
    try:
        prop_value1 = all['graphml']['graph']['node'][y]['data'][0]['#text']
    except KeyError as e:
        prop_value1 = ''
    try:
        prop_value2 = all['graphml']['graph']['node'][y]['data'][1]['#text']
    except KeyError as e:
        prop_value2 = ''
    try:
        prop_value3 = all['graphml']['graph']['node'][y]['data'][2]['#text']
    except KeyError as e:
        prop_value3 = ''
    print(node_label + ':{label:"' + prop_value1 + '",0:"'+ prop_value2 +'",1:"'+ prop_value3 +'"}')

