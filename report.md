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
