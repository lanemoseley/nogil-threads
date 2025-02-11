# Python 3.13: Disabling the global interpreter lock (GIL)

## Build cpython from source with --no-gil option

**This is done on my MacBook Pro with the M1 Pro chip.**

```
cd ~/Repositories
git clone https://github.com/python/cpython.git
cd cpython
```

```
git checkout 3.13
```

I had to install some missing dependencies:

```
brew install gdbm tcl-tk
```

Configure, specifying the correct paths for the header and library files for the missing dependencies:

```
./configure --prefix=$HOME/python-nogil --disable-gil \
    CPPFLAGS="-I$(brew --prefix gdbm)/include -I$(brew --prefix tcl-tk)/include" \
    LDFLAGS="-L$(brew --prefix gdbm)/lib -L$(brew --prefix tcl-tk)/lib"
```

We need to supply `make` with the number of available cores. For Mac, I used:

```
sysctl -n hw.ncpu
```

Then:

```
make -j8   # or, make -j$(sysctl -n hw.ncpu)
make install
```

Check that installation was successful:

```
~/python-nogil/bin/python3 -VV
Python 3.13.2+ experimental free-threading build (heads/3.13:aae0a1f9044, Feb  6 2025, 21:40:54) [Clang 16.0.0 (clang-1600.0.26.4)]
```

## Peformance Comparison

First, let's run `test_threads.py`. This is a simple program that increments a number using multiple threads.

Running this, we see a 71% improvement when using free-threading mode (GIL disabled).

```
➜  nogil-threads git:(main) ✗ python3 test_threads.py 
Execution Time: 2.05 seconds
➜  nogil-threads git:(main) ✗ ~/python-nogil/bin/python3 test_threads.py 
Execution Time: 0.60 seconds
```

### Fibonacci Sequence (`recursive_fibonacci.py`)

Calculating Fibonacci sequences recursively is CPU-intensive, but is also inherently single-threaded. We can see that free-threading mode actually performs much worse than regular Python with GIL enabled. This is due to the extra overhead of creating and managing function calls.

```
➜  nogil-threads git:(main) ✗ python3 recursive_fibonacci.py
Execution Time: 0.85 seconds
➜  nogil-threads git:(main) ✗ ~/python-nogil/bin/python3 recursive_fibonacci.py
Execution Time: 11.46 seconds
```

### Merge Sort (`merge_sort.py`)

Multithreaded merge sort is a more interesting example. Left and right subarrays are processed in parallel using separate threads. Each recursive call spawns new threads to sort subarrays independently before merging the results. Recursion is used with each left and right sub-array being processed by a separate thread. Python's GIL does not allow for true parallelism, which is why in this example free-threading mode consistently outperforms standard Python.

```
➜  nogil-threads git:(main) ✗ python3 merge_sort.py
Execution Time: 5.43 seconds
➜  nogil-threads git:(main) ✗ ~/python-nogil/bin/python3 merge_sort.py
Execution Time: 2.42 seconds
```

With the GIL enabled, execution time can vary widely due to thread contention and context switching overhead.

Even though we spawn multiple threads, the GIL forces them to wait for each other since only one thread at a time can execute Python bytecode. The time spent waiting for the GIL varies per run, causing inconsistent results.

```
➜  nogil-threads git:(main) ✗ python3 merge_sort.py
Execution Time: 5.43 seconds
➜  nogil-threads git:(main) ✗ ~/python-nogil/bin/python3 merge_sort.py
Execution Time: 2.42 seconds
```

```
➜  nogil-threads git:(main) ✗ python3 merge_sort.py                   
Execution Time: 19.39 seconds
➜  nogil-threads git:(main) ✗ ~/python-nogil/bin/python3 merge_sort.py
Execution Time: 2.64 seconds
```

```
➜  nogil-threads git:(main) ✗ python3 merge_sort.py                   
Execution Time: 13.56 seconds
➜  nogil-threads git:(main) ✗ ~/python-nogil/bin/python3 merge_sort.py
Execution Time: 2.29 seconds
```