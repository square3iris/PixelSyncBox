# ============================================
# FILE: pixel_sync/queue_manager.py
# VERSION: 1.1.0
# UPDATED: 2026-06-18
# ============================================
from queue import Queue


class UploadQueue:

    def __init__(self):

        self.queue = Queue()

    def add_files(self, files):

        for file in files:
            self.queue.put(file)

    def get(self):

        return self.queue.get_nowait()

    def done(self):

        self.queue.task_done()

    def empty(self):

        return self.queue.empty()

    def size(self):

        return self.queue.qsize()