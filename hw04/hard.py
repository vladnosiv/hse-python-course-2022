from datetime import datetime
import multiprocessing
import queue
import time
import codecs


def process_a(input_queue: multiprocessing.Queue,
              output_queue: multiprocessing.Queue):
    while True:
        try:
            msg = input_queue.get_nowait()
            output_queue.put(msg.lower())
        except queue.Empty:
            pass
        time.sleep(5)


def process_b(input_queue: multiprocessing.Queue,
              output_queue: multiprocessing.Queue):
    while True:
        try:
            msg = input_queue.get_nowait()
            output_queue.put(codecs.encode(msg, "rot_13"))
        except queue.Empty:
            pass
        time.sleep(5)


if __name__ == '__main__':
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    q3 = multiprocessing.Queue()

    multiprocessing.Process(target=process_a, args=(q1, q2), daemon=True).start()
    multiprocessing.Process(target=process_b, args=(q2, q3), daemon=True).start()

    while True:
        msg = input()
        print(f"Received the message from input: {msg}. Time: {datetime.now()}")
        q1.put(msg)
        encoded_msg = q3.get()
        print(f"Message is encoded: {encoded_msg}. Time: {datetime.now()}")
