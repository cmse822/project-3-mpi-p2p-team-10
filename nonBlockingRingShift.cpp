#include <ios>
#include <iostream>
#include <iomanip>
#include <mpi.h>

int main(int argc, char* argv[]) {
  // Initialize MPI
  MPI_Init(&argc, &argv);

  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  
  // Check for correct number of tasks
  if ((size & (size - 1)) != 0)
  {
    if (rank == 0)
      std::cout << "Invalid Number of Tasks!" << std::endl;
    MPI_Finalize();
    return 0;
  }

  // Check for message size and shift number arguments
  if (argc != 3)
  {
    if (rank == 0)
      std::cout << "Invalid Arguments!" << std::endl;
    MPI_Finalize();
    return 0;
  }

  // Get message size
  int messageSize = atoi(argv[1]);
  if (messageSize == 0 || (messageSize & (messageSize - 1)) != 0)
  {
    if (rank == 0)
      std::cout << "Invalid Message Size!" << std::endl;
    MPI_Finalize();
    return 0;
  }

  // Get shift number
  int shiftNum = atoi(argv[2]);
  if (shiftNum <= 0 || shiftNum >= size)
  {
    if (rank == 0)
      std::cout << "Invalid Shift Number!" << std::endl;
    MPI_Finalize();
    return 0;
  }

  // Create buffer for message sending / receiving
  char* sBuf = new char[messageSize];
  char* rBuf = new char[messageSize];

  MPI_Request sRequest;
  MPI_Request rRequest;
  int tests = 100000;
  double time = 0;
  double average = 0;
  double averages[64];
  
  // Perform _ runs to overcome statistical noise
  for (int t = 0; t < tests; ++t)
  {
    // Set starting data
    for (int i = 0; i < messageSize; ++i)
      sBuf[i] = rank + 'A';

    // Perform shiftNum data transfers around the ring
    time = MPI_Wtime();
    for (int i = 0; i < shiftNum; ++i)
    {
      int s = MPI_Isend(sBuf, messageSize, MPI_CHAR, (rank + 1) % size, 0, MPI_COMM_WORLD, &sRequest);
      int r = MPI_Irecv(rBuf, messageSize, MPI_CHAR, (rank + size - 1) % size, 0, MPI_COMM_WORLD, &rRequest);
      MPI_Wait(&sRequest, MPI_STATUS_IGNORE);
      MPI_Wait(&rRequest, MPI_STATUS_IGNORE);
      for (int j = 0; j < messageSize; ++j)
        sBuf[j] = rBuf[j];
    }
    time = MPI_Wtime() - time;
    average += time;

    // Check if shift works
    bool success = true;
    char expected = 'A' + (rank + size - shiftNum) % size;
    for (int i = 0; i < messageSize; ++i)
    {
      if (sBuf[i] != expected)
      {
        success = false;
        std::cout << "Rank " << rank << " didn't receive the correct data: " << sBuf[i] << " vs " << expected << std::endl; 
        break;
      }
    }
  }

  int root = 0;
  MPI_Gather(&average, 1, MPI_DOUBLE, &averages, 1, MPI_DOUBLE, root, MPI_COMM_WORLD);
  if (rank == 0)
  {
    average = 0;
    for (int i = 0; i < size; ++i)
    {
      average += averages[i];
    }
    std::cout << std::setw(2) << size << " "
              << std::setw(4) << messageSize << " "
              << std::setw(2) << shiftNum << " "
              << std::setw(12) << std::fixed << std::setprecision(10) << (average / (double)(tests * size)) << " "
              << std::setprecision(2) << (messageSize * shiftNum) / (average / (double)(tests * size)) << std::endl;
  }

  MPI_Barrier(MPI_COMM_WORLD);
  delete[] sBuf;
  delete[] rBuf;

  MPI_Finalize();

  return 0;
}
