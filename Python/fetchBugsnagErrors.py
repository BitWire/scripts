import json, re, requests, math, time

### User variables
#ProjectId
projectId = '--insert-Your-ProjectId--'
#ErrorId
errorId = '--Insert-Your-ErrorId--'
#Accesstoken Bugsnag
bugsnagToken = 'token ' + '--insert-Your-Data-Access-Token--'
#Full reports?
fullReports = True
#ResultFile, can get quite huge
resultFile = 'result.json'


### Code
bugsnagLink = 'https://api.bugsnag.com/projects/' + projectId + '/errors/' + errorId + '/events?per_page=30'

if fullReports == True:
    bugsnagLink += '&full_reports=true'

bugsnagHeaders = {'User-agent': 'BugsnagErrorDumper 0.1','Authorization': bugsnagToken}

r = requests.get(bugsnagLink, headers = bugsnagHeaders)

requestsLeft = r.headers['X-RateLimit-Remaining']
i = 1
while(True):
    if requestsLeft == "0":
        print('waiting for new requests')
        time.sleep(60)
    if "Link" not in r.headers:
        break
    if i != 1:
        linkHeader = r.headers['Link']
        links = re.findall(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", linkHeader)
        bugsnagLink = links[0][0]
    r = requests.get(bugsnagLink, headers = bugsnagHeaders)
    requestsLeft = r.headers['X-RateLimit-Remaining']
    print('Requests left:' + requestsLeft)
    f = open(resultFile, "w")
    f.write(json.dumps(r.json(), indent = 4))
    f.close()
    i += 1
