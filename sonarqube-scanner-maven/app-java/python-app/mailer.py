import json
import requests
import pprint

# TWO servers to compare
Servers = ("http://server1","http://server2")

# REST API for getting list of repos
REPO_LIST_API_PATH = "/api"


def main():
    repoLists = {}
    repoNames = {}
    serverDiff = {}
    serverDiff[Servers[0]] = []
    serverDiff[Servers[1]] = []

    # Fetch list of repo meta-data
    for server in Servers:
        print "Fetching repos from: " + server
        repoLists[server] = getRepos(server)
        print "--Found " + str(len(repoLists[server])) + " repos"

    # Convert to two sets of repo keys
    for server in Servers:
        repoNames[server] = getRepoNames(repoLists[server])

    # Find intersection of the two sets
    print "Comparing repos"
    repoDiff = set(repoNames[Servers[0]]).symmetric_difference(set(repoNames[Servers[1]]))

    for repo in repoDiff:
        if repo in repoNames[Servers[0]]:
            serverDiff[Servers[0]].append(repo)
        if repo in repoNames[Servers[1]]:
            serverDiff[Servers[1]].append(repo)

    print "Differences: "
    printObj(serverDiff)


def getRepoNames(repos):
    repoNames = []
    for repo in repos:
        repoNames.append(repo["key"])
    return repoNames


def getRepos(server):
    response = requests.get(server+REPO_LIST_API_PATH, headers={"content-type":"application/json","accept":"application/json"})
    return json.loads(response.text)


def printObj(object):
    print(pprint.pformat(object))

main()
