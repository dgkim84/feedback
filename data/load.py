import json
import requests

res = requests.post('http://localhost:3122/admin/projects', data={'name': 'Feedback', 'description': ''})
project = res.json()

items = json.loads(open('data/helloworld.json').read())
items.reverse()
for item in items:
  item['project'] = project['id']
  res = requests.post('http://localhost:3122/api/v1/tickets/', data=item)
