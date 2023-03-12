from update_loop import loop

import os
import requests
import base64

# specify the owner, repo, and path of the file you want to update
owner = 'ShockPlease'
repo = 'ShockPlease.github.io'
path = 'html/api/api.html'

# set up the Github API endpoint and retrieve the access token from a repository secret
api_endpoint = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
access_token = os.environ['TARKOV_TOKEN']

# make the API request to get the current content of the file
response = requests.get(api_endpoint.format(owner=owner, repo=repo, path=path), headers={'Authorization': 'Token ' + access_token})
response_json = response.json()

# get the current SHA of the file, which is needed to make the update
file_sha = response_json['sha']

loop()
new_content = open('data/data.json', 'r').read()
new_content_base64 = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

# make the API request to update the file
data = {
    'message': 'Update file',
    'content': new_content_base64,
    'sha': file_sha
}
response = requests.put(api_endpoint.format(owner=owner, repo=repo, path=path), json=data, headers={'Authorization': 'Token ' + access_token})

# print the response status code to make sure the update was successful
print(response.status_code)
