# Project 3
## Part 1 and 2
### Running the experiemnt
The implementaton of the ping-pong using MPI is available in  `ping-ping-blocking.c` and `ping-ping-non-blocking.c`.
To run the experiments required for part 1 and part 2 run the bash script `part_1_2_script.sh`.

### Results
The plots below visualize the time taken for the ping-pong exchange as a function of message size, comparing both blocking and non-blocking communication methods, and whether the communication happens within the same physical node or across different nodes.

![Blocking](assets/part_1_2/performance_comparison_blocking.png)

![Non-Blocking](assets/part_1_2/performance_comparison_non_blocking.png)

![ALL Together](assets/part_1_2/performance_comparison.png)

![ALL Together](assets/part_1_2/bandwidth.png)
### Analysis

- **Trend with Message Size**: For both blocking and non-blocking approaches, the time for communication increases with the size of the message. This is expected as larger messages require more time to be transmitted over the network bus. 

- **Same Node vs. Different Nodes**: Communication within the same node is significantly faster than between different nodes. This difference is due to the lower latency and higher bandwidth available within a single node. The impact of physical distance becomes more apparent as message sizes increase, leading to higher communication times for cross-node exchanges.

- **Blocking vs. Non-Blocking**: The non-blocking communication method generally shows similar or slightly higher times compared to the blocking method for smaller message sizes. However, as the message size increases, the non-blocking method can benefit from overlapped communication and computation, potentially reducing wait times. This is observed in the case of same-node communication but is less pronounced in cross-node communication due to higher network latencies.

- **Bandwidth**: Bandwidth can be inferred from the slope of the line in the log-log plot. A steeper slope indicates lower effective bandwidth because the time increases more rapidly with message size. The slope is generally steeper for different-node communication, indicating that bandwidth constraints are more significant in this scenario. 


#### Results Conclusion
 1. The non-blocking communication offers advantages in specific contexts, especially when managing large messages or when computation can be overlapped with message passing. However, the fundamental limitations of network latency and bandwidth are the primary determinants of performance.
 2. The difference between same-node and different-node communication underlines the importance of network characteristics in distributed computing environments.
 3. Our observations of bandwith trends show that bandwidth increases with message size. and while blocking and non-blocking modes show similar trends the communication within the same node achieves higher bandwidth.

## Part 4

You can find the code used for nonblocking ring shift in nonBlockingRingShift.cpp, and the code for plotting in plot_data.py.

To test the performance, the code was tested on the HPCC with 4 nodes, each utilizing up to 16 tasks. The time and bandwidth vs message size graphs are here:

![Time Vs Message Size](Q4_plot.png)

![Bandwidth Vs Message Size](Q4_plot_bandwidth.png)

### Analysis

As can be seen in the first figure, every curve has an upward trend as it takes longer to send larger messages; however, you will notice two distinct starting points yet a similar ending point. This is likely due to the lower (faster) curves being on the same node, hence they have lower latency (around 0.000001 seconds) and communicate faster on small message sizes compared to when there are more tasks which utilize multiple nodes, which then have to utilize the HPCC network (latency around 0.00001 seconds). Eventually they trend toward the same region/slope, indicating that the tasks become bound by the bandwidth moreso than latency.

This observation continues in the second figure, where the tasks with lower latency start with better bandwidth compared to the tasks with higher latency. As the message size increases, the bandwidths converge as they approach 1 GB/second, which is likely the maximum bandwidth available on the HPCC network.

Note that for both graphs, there are a couple of extreme outliers, which is unusual given that we tested the each RTT 10,000 times. After a couple tests, it appears there are always a few on the higher latency curves (not always the same). While we aren't sure of the exact cause, we hypothesize it has to do with the nodes the HPCC/MPI selected for that test.

Compared to blocking ring shift, nonblocking was faster, had lower latency/higher bandwidth, and better clustered curves. This is as expected, as the blocking protocol likely has more overhead due to its blocking nature, causing it to be slower than nonblocking. While some of the difference may be attributed to the HPCC nodes used, the results do follow what we expected. Overall, nonblocking appeared to have better performance (especially on smaller message sizes), but it comes at the cost of implementation complexity.
