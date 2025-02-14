import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "sync"
timeout = 120
loglevel = "info"
accesslog = "-"
errorlog = "-"
