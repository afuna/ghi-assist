import json
import requests
response = requests.post("http://127.0.0.1:8080",data=json.dumps({
    "comment": {
        "body": "##foo ##is: bug bar baz"
    },
    "issue": {
        "assignee": {},
        "url": "https://api.github.com/repos/afuna/dw-free/issues/12",
    },
}), headers={
    "X-Github-Event": "issue_comment",
    'Content-type': 'application/json'
}
)
print response.content