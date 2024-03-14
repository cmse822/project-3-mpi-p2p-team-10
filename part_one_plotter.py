import os
from matplotlib import pyplot as plt
import numpy as np
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


    bandwidth_results_all_configs = {}

for key, value in data.items():
    message_sizes_bytes = np.array(list(value.keys()))
    average_times_microseconds = np.array(list(value.values()))
    
    # Corrected bandwidth calculation in MB/s
    bandwidth_MB_s_corrected = (message_sizes_bytes * 2) / (average_times_microseconds * 1e-6 * (1024**2))
    
    # Update the dictionary with corrected results
    bandwidth_results_all_configs[key] = dict(zip(message_sizes_bytes, bandwidth_MB_s_corrected))

    # Prepare the plot for bandwidths
    fig, ax = plt.subplots(2, 1, figsize=(12, 14))

    # Loop through each configuration and plot its bandwidth
    for i, (config, bandwidth_data) in enumerate(bandwidth_results_all_configs.items()):
        message_sizes_bytes = np.array(list(bandwidth_data.keys()))
        bandwidth_MB_s = np.array(list(bandwidth_data.values()))
        
        ax[i // 2].plot(message_sizes_bytes, bandwidth_MB_s, label=config, marker='o')
        ax[i // 2].set_xscale('log', base=2)
        ax[i // 2].set_yscale('log', base=10)
        ax[i // 2].set_xlabel('Message Size (bytes)')
        ax[i // 2].set_ylabel('Bandwidth (MB/s)')
        ax[i // 2].set_title('Bandwidth vs Message Size (' + ('Non-Blocking' if 'NON-BLOCKING' in config else 'Blocking') + ')')
        ax[i // 2].grid(True, which="both", ls="--")
        ax[i // 2].legend()

    plt.tight_layout()
    plt.savefig('bandwidth.png')
