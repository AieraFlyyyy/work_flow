import hashlib
import json
import requests
import threading

dlsapce = 'https://space.bilibili.com/366511662/dynamic'
bilibili = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
params = {
    'visitor_uid': '0',
    'host_uid': '366511662',
    'offset_dynamic_id': '0',
    'need_top': '1',
    'platform': 'web'
}
corpId = 'ww4437a57a5011b511'
secretId = 'aCcnzlmNURGeuqML6hLmgFCI1XDPUp5YchKl_uT8HIY'

class WeChatPub:

    s = requests.session()

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpId}&corpsecret={secretId}"
        rep = self.s.get(url)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)['access_token']

    def send_msg(self, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "textcard",
            "agentid": 1000002,
            "textcard": {
                "title": "更新内容",
                "description": content,
                "url": dlsapce,
                "btntxt": "去看看"
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(
            form_data).encode('utf-8'), headers=header)
        if rep.status_code != 200:
            print("request failed.")
            return
        return json.loads(rep.content)

wechat = WeChatPub()

def checkUpdate():
    req = json.loads(requests.get(bilibili, params).text)
    data = req["data"]
    cards = data["cards"]
    first_card = cards[0]["card"]

    hash_code = hashlib.md5(first_card.encode('utf-8')).hexdigest()

    with open('data.txt', 'r') as file:
        data = file.read()

    description = json.loads(first_card)["item"]["description"]
    # wechat.send_msg(description)
    print(description)
    if(data != hash_code):
        with open('data.txt', 'w') as file_w:
            file_w.write(hash_code)
            wechat.send_msg(description)
    else:
        print('no update')


def fun_timer():
    print('Hello Timer!')
    checkUpdate()
    timer = threading.Timer(600, fun_timer)
    timer.start()

# fun_timer()
checkUpdate()
