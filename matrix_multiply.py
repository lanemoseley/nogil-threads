import random
import threading
import time

def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in A must match number of rows in B.")

    # Initialize result matrix with zeros
    C = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    # Matrix Multiplication
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]

   #  return C # discard result

def main():
   size = 200
   A = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
   B = [[random.randint(11, 20) for _ in range(size)] for _ in range(size)]

   num_threads = 8 # match number of available cores
   threads = []

   start_time = time.time()
   for _ in range(num_threads):
      t = threading.Thread(target=matrix_multiply, args=(A, B))
      t.start()
      threads.append(t)

   for t in threads:
      t.join()

   end_time = time.time()
   print(f"Execution Time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
   main()
