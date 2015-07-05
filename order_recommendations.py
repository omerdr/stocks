# input should be:
#   Firm,upgrade/downgrade, [Buy] -> [Sell]

# Run using:
# cd data
# cat marketbeat_nasdaq.csv | python ../parse_csv.py | awk -F, {'print $3","$4","$5'} | sort | uniq | grep -i "Upgrade\|Downgrade" | python ../order_recommendations.py out.jpg
# cat stocks.csv | python ../parse_csv.py | awk -F, '{ print $1","$2","$3","$4","$5"->"$6 }' | tail -n+2 | awk -F, {'print $3","$4","$5'} | sort | uniq | grep -i "Upgrade\|Downgrade" | python ../order_recommendations.py out_yahoo.jpg

FIRM_FIELD      = 0
ACTION_FIELD    = 1
FROM_TO_FIELD   = 2
OUTPUT_PS_FILENAME = 'out.jpg'

from sys import stdin, argv
import csv
import pygraphviz as pgv

def add_item(graph,key,val):
    if graph.has_key(key) and (not val in graph[key]):
        graph[key].append(val)
    else:
        graph[key] = [val]

def print_graph(graph, filename):
    G = pgv.AGraph(directed=True)
    G.add_nodes_from(graph)
    for k,vs in graph.iteritems():
        for v in vs:
            G.add_edge(k, v)
    print G

    for a in ['twopi', 'gvcolor', 'wc', 'ccomps', 'tred', 'sccmap', 'fdp', 'circo', 'neato', 'acyclic', 'nop', 'gvpr', 'dot', 'sfdp']:
        G.draw(filename, prog='dot',args='rankdir=BT')
        # try:
        #     G.draw('pics/' + a + '_' + filename, prog=a)
        # except Exception as e:
        #     print e.message

try:
    g = {}
    for l in csv.reader(stdin):
        if len(l) != 3:
            continue

        a = l[FROM_TO_FIELD].split('->')
        if len(a) != 2:
            continue

        a = [s.strip() for s in a]

        # add the edges to the graph
        # the links are pointing upwards (from lower to higher recommendation)
        if l[ACTION_FIELD].lower() == 'downgrade':
            add_item(g, a[1], a[0])
        elif l[ACTION_FIELD].lower == 'upgrade':
            add_item(g, a[0], a[1])

    print g
    out_filename = argv[1] if len(argv) > 1 else OUTPUT_PS_FILENAME
    print_graph(g, out_filename)
    print "Graph image saved to \'" + out_filename + "\'"

except KeyboardInterrupt:
    pass