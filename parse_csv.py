from sys import stdin
import csv

try:
    for l in csv.reader(stdin):
        for t in l:
            t = t.replace(",",";")
        print ",".join(l)
except (KeyboardInterrupt):
    pass