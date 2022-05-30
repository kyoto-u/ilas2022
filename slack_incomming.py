import os
import requests
import pprint
from dotenv import load_dotenv

load_dotenv()

server = os.environ.get("INCOMMING_URL")
data = {'text': 'python request test: atsumi'}

r = requests.post(server, json=data)

print('request data')
pprint.pprint(r.request.__dict__)

