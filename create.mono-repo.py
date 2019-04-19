import requests
import git
import os
import sys
import yaml

if len(sys.argv) == 3:
    repoYaml = sys.argv[1]
    workingDir = sys.argv[2]
else:
   print("Invalid Arguments")
   sys.exit()

#Retrieve list of repos from yaml file
stream = open(repoYaml,"r")
repoNames = yaml.load(stream)["repos"]
stream.close()     

#Now we create a new directory for our mono repo 
#and initialize an empty git repository inside of it
rw_dir = os.getcwd()  
repo_dir = os.path.join(rw_dir, workingDir)
file_name = os.path.join(repo_dir, 'README')

try:  
    os.mkdir(repo_dir)
except OSError:  
    print ("Creation of the directory %s failed" % repo_dir)
else:  
    print ("Successfully created the directory %s " % repo_dir)

monoRepo = git.Repo.init(repo_dir)
# This function just creates an empty file ...
open(file_name, 'wb').close()

# add the empty file to staging and then commit it
monoRepo.index.add([file_name])
monoRepo.index.commit("Initial commit: Creating Mono Repo")

#Hack needed to properly add subtrees
gitObj = monoRepo.git
gitObj.reset("--hard")

#Form cache of remotes already associated with this repo
#This should be empty
remoteNames = [remote.name for remote in monoRepo.remotes]
print(remoteNames)

for repo in repoNames:
    #Check to make sure potential remote is not already in cache
    if repo["name"] not in remoteNames:
        print("Remote does not exist: " , repo["name"])
        print("Creating remote for repo: " , repo["url"])
        monoRepo.create_remote(repo["name"], url=repo["url"])
    #add external repository as subdirectory under main repo
    gitObj().subtree('add' , repo["name"] , "master",prefix=repo["name"])
    


