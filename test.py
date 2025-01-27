import requests

# API URL
url = "http://127.0.0.1:5000/"

# Send GET request
# response = requests.get(url)

# # Print the response
# print(response.json())

import requests

# API URL
# url = url+"/index-document"

# # File path and metadata
# file_path = "./reliance_report.pdf"
# data = {
#     "share_name": "Reliance",
#     "date": "2025-01-25"
# }

# # Files to upload
# files = {
#     "file": open(file_path, "rb")
# }

# # Send POST request
# response = requests.post(url, data=data, files=files)

# # Print the response
# print(response.json())

# import requests

# API URL
url = url+"search"
print(url)

# Query parameters
params = {
    "query": "products and services",
    "share_name": "Reliance",  # Optional
    "k": 3                     # Optional
}

# Send GET request
response = requests.get(url, params=params)

# Print the response
print(response.json())

