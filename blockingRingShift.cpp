#include <mpi.h>
#include <iostream>
#include <string>
#include <cstring>

using namespace std;
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

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int message_size = 2;
    //Change default message size
    if(argc == 2) {
        message_size = stoi(argv[1]);
    }

    // Generate a message of certain size.
    char message[message_size];
    create_message(message, message_size);

    //TODO: Implement MPI_WTime()
    
    // Send data to the next process in the ring
    int prev_rank = (rank - 1 + size) % size; // Handle wraparound for rank 0
    int next_rank = (rank + 1) % size;
    MPI_Sendrecv(&message, message_size, MPI_CHAR, next_rank, 0, 
                 &message, message_size, MPI_CHAR, prev_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

    cout << "Rank " << rank << " received msg size: " << sizeof(message) << endl;

    MPI_Finalize();

    return 0;
}
