# graphConv
PG-to-RDF converter

## Usage
`graphConv.py -t input.graphml > output.ttl`

## Arguments
<pre>  file                a property graph file (eg. GraphML)
  -h, --help          show this help message and exit
  -t, --turtle        display output as RDF 1.1 Turtle
  -j, --jsonld        display output as JSON-LD 1.0
  -x, --rdfxml        display output as RDF 1.1 XML (old RDF/XML)
  -tl, --turtlelabel  display output as RDF 1.1 Turtle with labelled bnodes (N-Triple-like)
  -ct, --cturtle      display output as GZ compressed RDF 1.1 Turtle
  -cj, --cjsonld      display output as GZ compressed JSON-LD
  -cx, --crdfxml      display output as GZ compressed RDF 1.1 XML (old RDF/XML)
  -ctl, --cturtlel    display output as GZ compressed RDF 1.1 Turtle with labelled bnodes (N-Triple-like)
  -d, --display       display graph
  -y, --yarspg        YARS-PG flag
</pre>
