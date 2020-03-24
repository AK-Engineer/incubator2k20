import requests

roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vODI5MDZjODQtZDJkMS0zMTI1LTliMjUtNzg1YmVhYzY2NTlk'
token = 'YjY3YThkNDEtNWQzMS00ZjczLTgwMmEtZDgxZTY5Nzk0ZjUwOTgzMjZmYWUtZTQ1_PF84_consumer'

url = "https://api.ciscospark.com/v1/messages?roomId=" + roomId

header = {"content-type": "application/json; charset=utf-8", 
		  "authorization": "Bearer " + token}

response = requests.get(url, headers = header, verify = True)

print(response.json())