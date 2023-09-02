import csv

with open("RESULTS-rise-interp.csv") as f:
    reader = csv.DictReader(f)
    prev = None
    for row in reader:
        if prev and prev + 1 != int(row["count"]):
            print(prev, row)
        prev = int(row["count"])
    