"""
Course: CSE 351
Lesson: L01 Team Activity
File:   team01_threads.py
Author: Kyle Davies
Purpose: Find prime numbers

Instructions:

- Don't include any other Python packages or modules
- Review and follow the team activity instructions (team.md)

TODO 1) Get this program running.  Get cse351 package installed
TODO 2) move the following for loop into 1 thread
TODO 3) change the program to divide the for loop into 10 threads
TODO 4) change range_count to 100007.  Does your program still work?  Can you fix it?
Question: if the number of threads and range_count was random, would your program work?
"""

from datetime import datetime, timedelta
import threading
import random

# Include cse 351 common Python files
from cse351 import *

# Global variable for counting the number of primes found
prime_count = 0
numbers_processed = 0
prime_lock = threading.Lock()
processed_lock = threading.Lock()

def is_prime(n):
    """
        Primality test using 6k+-1 optimization.
        From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def worker(start, end):
    global prime_count
    global numbers_processed
    for i in range(start, end):
        with processed_lock:
            numbers_processed += 1
        if is_prime(i):
            with prime_lock:
                prime_count += 1
                print(i, end=', ', flush=True)
    print(flush=True)

def main():
    global prime_count
    global numbers_processed

    log = Log(show_terminal=True)
    log.start_timer()

    start_num = 10000000000
    range_count = 100000
    num_threads = 10
    numbers_processed = 0
    prime_count = 0

    # Calculate the size of each chunk for the threads
    chunk_size = range_count // num_threads
    remainder = range_count % num_threads

    threads = []
    start = start_num
    for i in range(num_threads):
        end = start + chunk_size
        if i < remainder:
            end += 1  # Distribute the remainder among the first few threads
        thread = threading.Thread(target=worker, args=(start, end))
        threads.append(thread)
        thread.start()
        start = end

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Should find 4306 primes
    log.write(f'Numbers processed = {numbers_processed}')
    log.write(f'Primes found      = {prime_count}')
    log.stop_timer('Total time')


if __name__ == '__main__':
    main()