import threading
import time

def recursive_fibonacci(n):
    if n <= 1:
        return n
    return recursive_fibonacci(n-1) + recursive_fibonacci(n-2)

def compute_fibonacci():
   recursive_fibonacci(30)

def main():
   num_threads = 8 # match number of available cores
   threads = []

   start_time = time.time()
   for _ in range(num_threads):
      t = threading.Thread(target=compute_fibonacci)
      t.start()
      threads.append(t)

   for t in threads:
      t.join()

   end_time = time.time()
   print(f"Execution Time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
