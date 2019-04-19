import yaml
import os
import sys
import requests

if len(sys.argv) == 3:
    user = sys.argv[1]
    yamlOutPath = sys.argv[2]
else:
    print("Invalid arguments")
    sys.exit()

stream = open(yamlOutPath + '.yaml', "w", encoding="utf-8")
req = 'https://api.github.com' + user + '/repos'
#Retrieve list of repos
response = requests.get(req)
#Filter out the repo names and urls and convert into a list of dictionaries
repoNames = [{"name": repos["name"] , "url": repos["git_url"]}  for repos in response.json()]
yaml.dump({"repos":repoNames} , stream ,default_flow_style=False)
print(yaml.dump({"repos":repoNames},default_flow_style=False))
stream.close()