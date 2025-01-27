import requests
import time

t1 = time.time()
# API URL
url = "https://chromadb-vercel-test.onrender.com/"

response = requests.get(url)
print(response.json())

t2 = time.time()

# API URL
index_url = url+"/index-document"
file_path = "./reliance_report.pdf"
data = {
    "share_name": "Reliance",
    "date": "2025-01-25"
}
files = {
    "file": open(file_path, "rb")
}

response = requests.post(index_url, data=data, files=files)
print(response.json())

t3 = time.time()

search_url = url+"search"
print(url)

# Query parameters
params = {
    "query": "products and services",
    "share_name": "Reliance",  # Optional
    "k": 3                     # Optional
}

# Send GET request
response = requests.get(search_url, params=params)
# Print the response
print(response.json())

t4 = time.time()

print("------")
print(f"/ time = {(t2-t1)}")
print(f"/index-document time : {(t3-t2)}")
print(f"/search : {(t4-t3)}")
print(f"TOTAL : {t4-t1}")