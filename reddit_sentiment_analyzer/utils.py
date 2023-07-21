from django.conf import settings
from configparser import ConfigParser
import os
import threading
from queue import Queue

THREADPOOL_LIMIT = 6

class ConfigReader:
    def __init__(self):
        self.configPath = os.path.join(settings.BASE_DIR, "projectConfig.ini")
        self.cf = ConfigParser()
        self.cf.read(self.configPath)

    def get(self, section, key):
        return self.cf.get(section, key)

class ThreadPool:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.lock = threading.Lock()
        self.threads = []


    def execute(self, func, *args, **kwargs):
        stop_event = threading.Event()
        thread = threading.Thread(target=self._execute_func, args=(func, stop_event,args, kwargs))
        thread.start()
        thread.sc = stop_event
        self._add_thread(thread)

    def _execute_func(self, func,stop_event, args, kwargs):
        try:
            func(stop_event, *args, **kwargs)
        except Exception as e:
            print(f"Error executing function: {e}")

        self._remove_thread(threading.current_thread())

    def _add_thread(self, thread):
        with self.lock:
            self.threads.append(thread)

    def _remove_thread(self, thread):
        with self.lock:
            self.threads.remove(thread)

    def view_running_threads(self):
        with self.lock:
            return self.threads

    def destroy_thread(self, thread):
        with self.lock:
            if thread in self.threads:
                thread.sc.set()
                thread.join()
                self.threads.remove(thread)

    def destroy_all_threads(self):
        with self.lock:
            for thread in self.threads:
                thread.sc.set()
                thread.join()

            self.threads.clear()


class SingletonQueue:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.lock = threading.Lock()
        self.queue = Queue()

    def enqueue(self, value):
        self.queue.put(value)

    def fetch(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None