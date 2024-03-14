import os
from matplotlib import pyplot as plt
data = {}




if __name__ == "__main__":
    for file in os.listdir("."):
        if file.startswith("slurm"):
            with open(file) as temp_file:
                file_lines = temp_file.readlines()
                for line in file_lines :
                    if "JobName" in line:
                        job_name = line.split("JobName=")[-1].strip()
                        break
                else:
                    print("JobnName not found")

                if job_name not in data:
                    data[job_name] = {}
                for line in file_lines: 
                    if "|" in line and len(line) < 20:
                        data_size, time = map(float,line.split("|"))
                        if data_size > 1:
                            if data_size not in data[job_name]:
                                data[job_name][data_size] = []                
                            data[job_name][data_size].append(time)
                        
    for job_name in data.keys():
        for size in data[job_name].keys():
            data[job_name][size] = sum(data[job_name][size]) / len(data[job_name][size]) 

    print(data)
    plt.figure(figsize=(10, 8))

    for key, value in data.items():
        sizes = list(value.keys())
        times = list(value.values())
        if "NON-BLOCKING" in key:
            plt.plot(sizes, times, marker='o', linestyle='-', label=key)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Size')
    plt.ylabel('Time (s)')
    plt.title('Performance Comparison')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig('performance_comparison_blocking.png')


    plt.figure(figsize=(10, 8))

    for key, value in data.items():
        sizes = list(value.keys())
        times = list(value.values())
        if not "NON-BLOCKING" in key:
            plt.plot(sizes, times, marker='o', linestyle='-', label=key)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Size')
    plt.ylabel('Time (s)')
    plt.title('Performance Comparison')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig('performance_comparison_non_blocking.png')
