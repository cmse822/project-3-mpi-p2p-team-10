#include <mpi.h>
#include <iostream>
#include <string>
#include <cstring>
#include <vector>

/**
 * Generate a messsage of given size in bytes when given a char array.
 * 
 * @param message message array
 * @param size size of the message array in bytes
*/
void create_message(char message[], int size) {
  memset(message, 'a', size);
  message[size] = '\0';
}

int main(int argc, char* argv[]) {
  MPI_Init(&argc, &argv);
  double start_time, end_time, total_time;
  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  int message_size = 1; // size of message in bytes
  int shifts = 1; // how many ring shifts to do
  
  if(argc == 2) {
    message_size = std::stoi(argv[1]);
  }
  if(argc == 3) {
    message_size = std::atoi(argv[1]);
    shifts = std::stoi(argv[2]);
  }
  
  // Generate a message of certain size.
  char message[message_size];
  // std::vector<char> message(message_size);
  create_message(message, message_size);

  // Send data to the next process in the ring
  int prev_rank = (rank - 1 + size) % size; // Handle wraparound for rank 0
  int next_rank = (rank + 1) % size;

  // Run for 1000 iterations
  for (int i = 0; i < 1000; i++){
    // Ensure all process start at same time
    MPI_Barrier(MPI_COMM_WORLD);
    start_time = MPI_Wtime(); 

    // MPI_Sendrecv(message.data(), message.size(), MPI_CHAR, next_rank, 0, 
    //              message.data(), message.size(), MPI_CHAR, prev_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    for (int s = 0; s < shifts; s++) {
    MPI_Sendrecv(&message, message_size, MPI_CHAR, next_rank, 0,
                 &message, message_size, MPI_CHAR, prev_rank, 0,
                 MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    // std::cout << "Rank " << rank << " received msg size: " << sizeof(message) << std::endl;

    // Ensure all process end at same time
    MPI_Barrier(MPI_COMM_WORLD);
    end_time = MPI_Wtime(); 

    // Master node records time for ring shift to work.
    if(rank == 0) {
      double elapsed_time = end_time - start_time;
      total_time += elapsed_time;
    }
  }

  // Master node does calculations
  if (rank == 0){
    double avg_time = total_time / 1000;
    // double bandwidth = message_size*2 / avg_time;
    std::cout << size << " " << message_size << " " << avg_time << std::endl;
  }
  
  MPI_Finalize();
  return 0;
}
