import requests
import pprint

server = 'https://hooks.slack.com/services/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'
data = {'text': 'python request test: atsumi'}

r = requests.post(server, json=data)

print('request data')
pprint.pprint(r.request.__dict__)

