import csv

input_file = open("RESULTS-rise.csv")
reader = csv.DictReader(input_file)

print(reader.fieldnames)
prev_row = None

with open("RESULTS-rise-interp.csv", "w", newline="") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        # interpolate the missing rows
        if prev_row and int(prev_row["count"]) + 1 != int(row["count"]):
            keep_vals = [fieldname for fieldname in reader.fieldnames if fieldname != 'ts(ms)' and fieldname != 'count']
            for i in range(int(prev_row["count"]) + 1, int(row["count"])):
                new_row = {}
                new_row["count"] = i
                new_row['ts(ms)'] = float(prev_row['ts(ms)']) + (float(row['ts(ms)']) - float(prev_row['ts(ms)'])) / (int(row["count"]) - int(prev_row["count"])) * (i - int(prev_row["count"]))
                for val in keep_vals:
                    new_row[val] = prev_row[val]
                writer.writerow(new_row)
        
        writer.writerow(row)
        prev_row = row
        
input_file.close()
