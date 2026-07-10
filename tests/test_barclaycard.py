from monitors.barclaycard import BarclaycardMonitor

monitor = BarclaycardMonitor()

result = monitor.collect()

print(result)