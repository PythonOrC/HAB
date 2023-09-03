import csv


exp_dataset = open("collected-data.csv", "r")
exp_reader = csv.reader(exp_dataset)
exp_content = [row for row in exp_reader]
exp_count_col = [row[14] for row in exp_content]
exp_alt_col = [row[11] for row in exp_content]
exp_count = []
exp_alt = []
for i in range(len(exp_count_col)):
    if exp_count_col[i] == "CountRate":
        continue
    if exp_count_col[i] == '':
        break
    exp_count.append(float(exp_count_col[i].strip()))
    exp_alt.append(exp_alt_col[i])
max_exp_count = max(exp_count)

sim_dataset = open("Simulation Result.csv", "r")
sim_reader = csv.reader(sim_dataset)
sim_content = [row for row in sim_reader]
sim_count_col = [row[1] for row in sim_content]
sim_count = []
for i in range(len(sim_count_col)):
    if sim_count_col[i] != "" and sim_count_col[i] != "count":
        sim_count.append(float(sim_count_col[i].strip()))
max_sim_count = max(sim_count)


manual_reduce_factor = 0.95

reduce_factor = max_exp_count / max_sim_count * manual_reduce_factor



print("Max experimental count: ", max_exp_count)
print("Max simulated count: ", max_sim_count)
print("Reduce factor: ", reduce_factor)

with open("Simulation Result resized.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Altitude (m)", "Resized Sim Count", "Exp Count"])
    max = 0
    
    for i in range(1, 283):
        alt = sim_content[i][0]

        exp_count_alt = exp_count[exp_alt.index(alt)] if alt in exp_alt else ""
        
        writer.writerow([alt, float(sim_content[i][1]) * reduce_factor, exp_count_alt])
        if float(sim_content[i][1]) * reduce_factor > max:
            max = int(sim_content[i][1]) * reduce_factor
    
    
    
    # for row in sim_content[1:]:
    #     writer.writerow([row[0], row[1], float(row[1]) * reduce_factor])
    #     if float(row[1]) * reduce_factor > max:
    #         max = int(row[1]) * reduce_factor
    print("Max resized altitude: ", max)
