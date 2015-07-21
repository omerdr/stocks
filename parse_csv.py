from sys import stdin
import csv

try:
    for l in csv.reader(stdin):
        for i in range(len(l)):
            l[i] = l[i].replace(",",";")
        print ",".join(l)
except (KeyboardInterrupt):
    pass