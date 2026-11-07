# Chapter 2: Advanced Thread Synchronization

## Overview
This script demonstrates an advanced implementation of the **Producer-Consumer architecture** in Python. It combines two fundamental synchronization primitives from Chapter 2: `queue.Queue` and `threading.Event`. 

To make the demonstration practical, the script simulates an asynchronous security logging pipeline where one thread generates threat alerts and another processes them. This mirrors real-world security infrastructure, such as endpoint agents continuously sending telemetry to a central SIEM manager for active threat monitoring.

## Key Concepts Demonstrated

* **Thread-Safe Data Transfer (`queue.Queue`):** 
  Instead of using a standard Python list (which can suffer from race conditions), this script uses `queue.Queue`. The Queue manages memory locks automatically, allowing the `LogProducer` to safely `.put()` data while the `LogConsumer` concurrently uses `.get()` to retrieve it.
  
* **Graceful Shutdown Signaling (`threading.Event`):**
  A common issue in Producer-Consumer scripts is the Consumer getting stuck in an infinite `while True:` loop, requiring a forced termination. This code solves that by passing a `threading.Event` flag. Once the Producer finishes its loop, it calls `event.set()`. The Consumer checks this flag and shuts down cleanly once the queue is empty, preventing memory leaks and dangling threads.

* **Thread-Safe Output (`logging` vs `print`):**
  The `logging` module is used instead of standard `print()` statements because `logging` is thread-safe in Python. This guarantees that console outputs from simultaneous threads do not overwrite each other or break onto the same line.

## Execution Output
Running the script via the terminal produces a real-time execution timeline:

```text
2026-11-08 01:33:34,895 ProducerThread  INFO     Generated and queued alert: Failed_Login
2026-11-08 01:33:34,896 ConsumerThread  INFO     Processing alert: Failed_Login
2026-11-08 01:33:35,855 ProducerThread  INFO     Generated and queued alert: Malware_Detected
2026-11-08 01:33:35,855 ConsumerThread  INFO     Processing alert: Malware_Detected
2026-11-08 01:33:36,676 ProducerThread  INFO     Generated and queued alert: Malware_Detected
2026-11-08 01:33:36,676 ConsumerThread  INFO     Processing alert: Malware_Detected
2026-11-08 01:33:37,247 ProducerThread  INFO     Generated and queued alert: Failed_Login
2026-11-08 01:33:37,247 ConsumerThread  INFO     Processing alert: Failed_Login
2026-11-08 01:33:38,035 ProducerThread  INFO     Generated and queued alert: Malware_Detected
2026-11-08 01:33:38,035 ConsumerThread  INFO     Processing alert: Malware_Detected
2026-11-08 01:33:38,036 ProducerThread  INFO     Finished generating alerts. Setting stop event.
2026-11-08 01:33:38,562 ConsumerThread  INFO     Consumer shutting down gracefully.
2026-11-08 01:33:38,564 MainThread      INFO     Pipeline execution successfully completed.

## Understanding the Execution Flow
- **Data Handoff:** The logs show that milliseconds after the `ProducerThread` wakes up and queues a random security event, the `ConsumerThread` pulls it from the shared Queue and processes it. This generation and consumption cycle executes 5 times.
- **The Signaling Event:** After queuing the 5th alert, the Producer announces it is finished and triggers the `threading.Event()` flag. This acts as a control signal to the Consumer that the pipeline is closing.
- **Graceful Exit:** Because the event flag was triggered, the Consumer knows no more logs are coming. It finishes processing the final alert and shuts down cleanly, followed by the Main Thread closing the program. This completely avoids hanging processes.

