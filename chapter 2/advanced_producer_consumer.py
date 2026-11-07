"""
Advanced Producer-Consumer Pipeline using Queue and Event
Demonstrates thread-safe data transfer and graceful shutdown signaling.
"""

import threading
import queue
import time
import random
import logging

# Configure thread-safe logging
LOG_FORMAT = '%(asctime)s %(threadName)-15s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

class LogProducer(threading.Thread):
    def __init__(self, log_queue, stop_event):
        super().__init__(name="ProducerThread")
        self.log_queue = log_queue
        self.stop_event = stop_event

    def run(self):
        # Simulating the generation of system alerts
        alert_types = ["Failed_Login", "Malware_Detected", "Port_Scan", "Privilege_Escalation"]
        
        for _ in range(5):
            time.sleep(random.uniform(0.5, 1.2))
            alert = random.choice(alert_types)
            self.log_queue.put(alert)
            logging.info(f"Generated and queued alert: {alert}")
        
        logging.info("Finished generating alerts. Setting stop event.")
        # Signal the consumer that no more items will be produced
        self.stop_event.set()

class LogConsumer(threading.Thread):
    def __init__(self, log_queue, stop_event):
        super().__init__(name="ConsumerThread")
        self.log_queue = log_queue
        self.stop_event = stop_event

    def run(self):
        # Keep running until the stop event is set AND the queue is completely empty
        while not self.stop_event.is_set() or not self.log_queue.empty():
            try:
                # Timeout prevents the thread from blocking forever if the queue is empty
                alert = self.log_queue.get(timeout=0.5)
                logging.info(f"Processing alert: {alert}")
                time.sleep(random.uniform(0.2, 0.6))  # Simulate processing time
                self.log_queue.task_done()
            except queue.Empty:
                continue
                
        logging.info("Consumer shutting down gracefully.")

if __name__ == "__main__":
    # Initialize the shared resources
    pipeline_queue = queue.Queue()
    shutdown_signal = threading.Event()

    # Initialize threads
    producer = LogProducer(pipeline_queue, shutdown_signal)
    consumer = LogConsumer(pipeline_queue, shutdown_signal)

    # Start threads
    producer.start()
    consumer.start()

    # Wait for both threads to complete execution
    producer.join()
    consumer.join()
    
    logging.info("Pipeline execution successfully completed.")