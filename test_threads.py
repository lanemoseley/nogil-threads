import threading
import time

def compute():
    x = 0
    for _ in range(10**7):
        x += 1

def main():
    num_threads = 8 # match number of available cores
    threads = []

    start_time = time.time()
    for _ in range(num_threads):
        t = threading.Thread(target=compute)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
