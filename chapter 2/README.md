# Chapter 2: Advanced Thread Synchronization

## Overview
This script demonstrates an advanced implementation of the **Producer-Consumer architecture** in Python. It combines two fundamental synchronization primitives from Chapter 2: `queue.Queue` and `threading.Event`. 

To make the demonstration practical, the script simulates an asynchronous security logging pipeline where one thread generates threat alerts and another processes them.

## Key Concepts Demonstrated

* **Thread-Safe Data Transfer (`queue.Queue`):** 
  Instead of using a standard Python list (which can suffer from race conditions), this script uses `queue.Queue`. The Queue manages memory locks automatically, allowing the `LogProducer` to safely `.put()` data while the `LogConsumer` concurrently uses `.get()` to retrieve it.
  
* **Graceful Shutdown Signaling (`threading.Event`):**
  A common issue in Producer-Consumer scripts is the Consumer getting stuck in an infinite `while True:` loop, requiring a forced termination. This code solves that by passing a `threading.Event` flag. Once the Producer finishes its loop, it calls `event.set()`. The Consumer checks this flag and shuts down cleanly once the queue is empty, preventing memory leaks and dangling threads.

* **Thread-Safe Output (`logging` vs `print`):**
  The `logging` module is used instead of standard `print()` statements because `logging` is thread-safe in Python. This guarantees that console outputs from simultaneous threads do not overwrite each other or break onto the same line.

## How to Run
Execute the script via the terminal:
```bash
python advanced_producer_consumer.py