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
import yaml
import rdflib
import json
import zlib
import gzip
import io
import codecs
from rdflib import Graph, plugin
import json, rdflib_jsonld
from rdflib.plugin import register, Serializer
register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')

def writeStdErr(message):
    sys.stderr.write(message)

if sys.version_info[0] < 3:
    writeStdErr('\nPython2 is not supported\n')
    exit()

parser = argparse.ArgumentParser(description='PG-to-RDF Converter', usage=sys.argv[0] + ' -t input.graphml > output.ttl')
parser.add_argument('file', type=str, help='a property graph file (eg. GraphML)')
parser.add_argument("-t", "--turtle", help="display output as RDF 1.1 Turtle",
                    action="store_true")
parser.add_argument("-j", "--jsonld", help="display output as JSON-LD 1.0",
                    action="store_true")
parser.add_argument("-x", "--rdfxml", help="display output as RDF 1.1 XML (old RDF/XML)",
                    action="store_true")
parser.add_argument("-tl", "--turtlelabel", help="display output as RDF 1.1 Turtle with labelled bnodes (N-Triple-like)",
                    action="store_true")
parser.add_argument("-ct", "--cturtle", help="display output as GZ compressed RDF 1.1 Turtle",
                    action="store_true")
parser.add_argument("-cj", "--cjsonld", help="display output as GZ compressed JSON-LD",
                    action="store_true")
parser.add_argument("-cx", "--crdfxml", help="display output as GZ compressed RDF 1.1 XML (old RDF/XML)",
                    action="store_true")
parser.add_argument("-ctl", "--cturtlel", help="display output as GZ compressed RDF 1.1 Turtle with labelled bnodes (N-Triple-like)",
                    action="store_true")
parser.add_argument("-d", "--display", help="display graph",
                    action="store_true")
parser.add_argument("-y", "--yarspg", help="YARS-PG flag",
                    action="store_true")
args = parser.parse_args()

if args.file and not args.yarspg:
  with open(args.file, 'r') as content_file:
    try:
        content = content_file.read()
        all = xmltodict.parse(content, process_namespaces=False)
    except:
        writeStdErr('It looks like you pointed to a file that is not GraphML\n')
        exit()

    graph_blank = str(uuid.uuid4())

    serttl = ''
    serttl = serttl + '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
    serttl = serttl + '@prefix pgo: <http://ii.uwb.edu.pl/pgo/> .\n'
    serttl = serttl + '\n'
    sery = ''

    for x in range(len(all['graphml']['graph']['edge'])):
        edge_label = all['graphml']['graph']['edge'][x]['@id']
        edge_source = all['graphml']['graph']['edge'][x]['@source']
        edge_target = all['graphml']['graph']['edge'][x]['@target']
        edge_blank = str(uuid.uuid4())
        serttl = serttl + '_:'+ graph_blank +' a pgo:PropertyGraph ;\n'
        serttl = serttl + '  pgo:hasEdge _:' + edge_blank + ' .\n'
        serttl = serttl + '\n'
        serttl = serttl + '_:' + edge_blank + ' a pgo:Edge ;\n'
        serttl = serttl + '  pgo:label "'+ edge_label + '" ;\n'
        serttl = serttl + '  pgo:startNode _:' + edge_source + ' ;\n'
        serttl = serttl + '  pgo:endNode _:' + edge_target + ' .\n'
        sery = sery + '(' + edge_source + ')-[]->(' + edge_target + ')\n'

    for y in range(len(all['graphml']['graph']['node'])):
        node_label = all['graphml']['graph']['node'][y]['@id']
        prop_blank1 = str(uuid.uuid4())
        prop_blank2 = str(uuid.uuid4())
        prop_blank3 = str(uuid.uuid4())
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
        except IndexError as e:
            prop_value3 = ''
        serttl = serttl + '\n'
        serttl = serttl + '_:' + node_label + ' a pgo:Node ;\n'
        serttl = serttl + '  pgo:label "' + node_label +'" ;\n'
        serttl = serttl + '  pgo:hasProperty _:' + prop_blank1 + ' , _:'+ prop_blank2 + ' , _:'+ prop_blank3 + ' .\n'
        serttl = serttl + '\n'
        serttl = serttl + '_:' + prop_blank1 + ' a pgo:Property ;\n'
        serttl = serttl + '  pgo:key "label" ;\n'
        serttl = serttl + '  pgo:value "' + prop_value1 + '" .\n'
        serttl = serttl + '_:' + prop_blank2 + ' a pgo:Property ;\n'
        serttl = serttl + '  pgo:key "0" ;\n'
        serttl = serttl + '  pgo:value "' + prop_value2 + '" .\n'
        serttl = serttl + '_:' + prop_blank3 + ' a pgo:Property ;\n'
        serttl = serttl + '  pgo:key "1" ;\n'
        serttl = serttl + '  pgo:value "' + prop_value3 + '" .\n'
        sery = sery + node_label + ':{label:"' + prop_value1 + '",0:"'+ prop_value2 +'",1:"'+ prop_value3 +'"}\n'

    g = Graph()
    g.parse(data=serttl,format='turtle')
    if args.rdfxml:
        print(g.serialize(format='xml').decode("utf-8"))
    elif args.jsonld:
        print(g.serialize(format='json-ld',indent=0).decode("utf-8"))
    elif args.turtlelabel:
        print(g.serialize(format='nt').decode("utf-8"))
    elif args.cturtle:
        filename = 'output.ttl.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='turtle').decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.cjsonld:
        filename = 'output.jsonld.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='json-ld',indent=0).decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.crdfxml:
        filename = 'output.rdf.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='xml').decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.cturtlel:
        filename = 'outputl.ttl.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='nt').decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.display:
        print(sery)
    else:
        print(g.serialize(format='turtle').decode("utf-8"))
else:
    with open(args.file, 'r') as stream:
        try:
            all = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit()

    graph_blank = str(uuid.uuid4())

    serttl = ''
    serttl = serttl + '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
    serttl = serttl + '@prefix pgo: <http://ii.uwb.edu.pl/pgo/> .\n'
    serttl = serttl + '\n'
    sery = ''
    
    for x in range(len(all['e'])):
        edge_label = all['e'][x]['id']
        edge_source = all['e'][x]['s']
        edge_target = all['e'][x]['t']
        edge_blank = str(uuid.uuid4())
        serttl = serttl + '_:'+ graph_blank +' a pgo:PropertyGraph ;\n'
        serttl = serttl + '  pgo:hasEdge _:' + edge_blank + ' .\n'
        serttl = serttl + '\n'
        serttl = serttl + '_:' + edge_blank + ' a pgo:Edge ;\n'
        serttl = serttl + '  pgo:label "'+ edge_label + '" ;\n'
        serttl = serttl + '  pgo:startNode _:' + edge_source + ' ;\n'
        serttl = serttl + '  pgo:endNode _:' + edge_target + ' .\n'
        sery = sery + '(' + edge_source + ')-[]->(' + edge_target + ')\n'

    for y in range(len(all['n'])):
        node_label = all['n'][y]['id']
        prop_blank1 = str(uuid.uuid4())
        prop_blank2 = str(uuid.uuid4())
        prop_blank3 = str(uuid.uuid4())
        try:
            prop_value1 = all['n'][y]['d'][0]
        except KeyError as e:
            prop_value1 = ''
        try:
            prop_value2 = all['n'][y]['d'][1]
        except KeyError as e:
            prop_value2 = ''
        try:
            prop_value3 = all['n'][y]['d'][2]
        except KeyError as e:
            prop_value3 = ''
        except IndexError as e:
            prop_value3 = ''
        serttl = serttl + '\n'
        serttl = serttl + '_:' + node_label + ' a pgo:Node ;\n'
        serttl = serttl + '  pgo:label "' + node_label +'" ;\n'
        serttl = serttl + '  pgo:hasProperty _:' + prop_blank1 + ' , _:'+ prop_blank2 + ' , _:'+ prop_blank3 + ' .\n'
        serttl = serttl + '\n'
        serttl = serttl + '_:' + prop_blank1 + ' a pgo:Property ;\n'
        serttl = serttl + '  pgo:key "label" ;\n'
        serttl = serttl + '  pgo:value "' + prop_value1 + '" .\n'
        serttl = serttl + '_:' + prop_blank2 + ' a pgo:Property ;\n'
        serttl = serttl + '  pgo:key "0" ;\n'
        serttl = serttl + '  pgo:value "' + prop_value2 + '" .\n'
        serttl = serttl + '_:' + prop_blank3 + ' a pgo:Property ;\n'
        serttl = serttl + '  pgo:key "1" ;\n'
        serttl = serttl + '  pgo:value "' + prop_value3 + '" .\n'
        sery = sery + node_label + ':{label:"' + prop_value1 + '",0:"'+ prop_value2 +'",1:"'+ prop_value3 +'"}\n'

    g = Graph()
    g.parse(data=serttl,format='turtle')
    if args.rdfxml:
        print(g.serialize(format='xml').decode("utf-8"))
    elif args.jsonld:
        print(g.serialize(format='json-ld',indent=0).decode("utf-8"))
    elif args.turtlelabel:
        print(g.serialize(format='nt').decode("utf-8"))
    elif args.cturtle:
        filename = 'output.ttl.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='turtle').decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.cjsonld:
        filename = 'output.jsonld.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='json-ld',indent=0).decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.crdfxml:
        filename = 'output.rdf.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='xml').decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.cturtlel:
        filename = 'outputl.ttl.gz'
        with gzip.open(filename, 'wb') as f:
            data = g.serialize(format='nt').decode()
            f.write(data.encode('utf-8'))
        print('File ' + filename + ' created')
    elif args.display:
        print(sery)
    else:
        print(g.serialize(format='nt').decode("utf-8"))
