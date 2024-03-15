import matplotlib.pyplot as plt
import os
import numpy as np



def main():
    task_list = [2, 4, 8, 16, 32, 64, 128]
    plt.figure(figsize=(10, 6))
    for task in task_list:
        x = []
        y = []
        file_name = "tasks.out"
        file_name = str(task) + file_name
        with open(file_name, "r") as file:
            for line in file:
                words = line.strip().split()  # Remove trailing whitespace and split by spaces
                # Process the words in the 'words' list
                x.append(float(words[1]))
                y.append(float(words[2]))
        plt.plot(x, y, marker='o', label=str(task)+" nodes")
        
    # Set up the plot
    plt.legend()
    plt.yscale("log")
    plt.xscale("log")
    plt.title(f"Blocking Ring Shift Performance(1 shift)")
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.savefig('1blockingringshift_plot.png')

    # reset for next plot
    plt.clf()
    for task in task_list:
        x = []
        y = []
        file_name = "tasks1000shifts.out"
        file_name = str(task) + file_name
        with open(file_name, "r") as file:
            for line in file:
                words = line.strip().split()  # Remove trailing whitespace and split by spaces
                # Process the words in the 'words' list
                x.append(float(words[1]))
                y.append(float(words[2]))
        plt.plot(x, y, marker='o', label=str(task)+" nodes")

    # Set up the plot
    plt.legend()
    plt.yscale("log")
    plt.xscale("log")
    plt.title(f"Blocking Ring Shift Performance(1000 shift)")
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.savefig('1000blockingringshifts_plot.png')

    

if __name__ == "__main__":
    main()