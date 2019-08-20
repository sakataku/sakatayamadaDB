import json,requests
# coding: utf-8
post_data = {
            "title": "山田",
            "url" : "https://yamada/",
            "overview" : "山田あーきひこ",
            "keyword" : "やまでん"
        }

url = 'http://ec2-52-194-247-170.ap-northeast-1.compute.amazonaws.com/data_insert'
headers = {'content-type': 'application/json'}
response = requests.post(url, json.dumps(post_data), headers=headers)
print(response.text)

