import requests
import time

url = 'http://127.0.0.1:8000/api/animals/'

start_time = time.time()

response = requests.get(url=url)
duration = time.time() - start_time
print(f'Response Time {duration}')