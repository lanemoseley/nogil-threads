import random
import threading
import time

def merge(left, right):
   # merge two sorted lists into single sorted list
   result = []
   i, j = 0, 0

   while i < len(left) and j < len(right):
      if left[i] < right[j]:
         result.append(left[i])
         i += 1
      else:
         result.append(right[j])
         j += 1

   while i < len(left):
      result.append(left[i])
      i += 1
   while j < len(right):
      result.append(right[j])
      j += 1

   return result

def merge_sort(arr):
   if len(arr) <= 1:
      return arr

   mid = len(arr) // 2

   left = arr[:mid]
   right = arr[mid:]

   sorted_left = []
   sorted_right= []

   # use function wrappers to allow threads to modify lists in enclosing scope
   # this allows us to get the results from the thread
   def sort_left():
      nonlocal sorted_left
      sorted_left = merge_sort(left)

   def sort_right():
      nonlocal sorted_right
      sorted_right = merge_sort(right)

   left_thread = threading.Thread(target=sort_left)
   right_thread = threading.Thread(target=sort_right)

   left_thread.start()
   right_thread.start()

   left_thread.join()
   right_thread.join()

   return merge(sorted_left, sorted_right)


def main():
   big_list = random.sample(range(1, 10_000), 3_000)
   start_time = time.time()
   result = merge_sort(big_list)
   end_time = time.time()
   print(f"Execution Time: {end_time - start_time:.2f} seconds")
   assert result == sorted(big_list), "Sort failed... Incorrect results."


if __name__ == '__main__':
   main()
