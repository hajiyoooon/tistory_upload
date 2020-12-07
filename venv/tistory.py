import requests
import re
from bs4 import BeautifulSoup
import json


class Tistory:
    def __init__(self, args):
        self.client_id = args[0]
        self.client_secret = args[1]
        self.callback_url = args[2]
        self.id = args[3]
        self.passwd = args[4]

        self.oauth_url = "https://www.tistory.com/oauth/authorize"
        self.login_url = 'https://www.tistory.com/auth/login'
        self.access_token_url = "https://www.tistory.com/oauth/access_token"

    def get_authentication_code(self):
        req_params = {'client_id': self.client_id,
                      'redirect_uri': self.callback_url,
                      'response_type': 'code'}

        login_info = {'loginId': self.id,
                      'password': self.passwd}

        acc_token_params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.callback_url,
            'grant_type': 'authorization_code'
        }
        
        with requests.session() as s:
            res = s.post(self.login_url, data=login_info)
            res = s.get(self.oauth_url, params=req_params, allow_redirects=False)

            bs = BeautifulSoup(res.text, 'html.parser')
            

            p = re.compile("(?<=\?code=)[a-zA-Z:/0-9?=]*")
            m = p.search(bs.select("head > script")[0].string)
            acc_token_params['code'] = m.group()

            res = s.get(self.access_token_url, params=acc_token_params)

            if (res.status_code == 200):
                received = res.text
                p = re.compile("(?<=access_token=)\w+")
                m = p.search(received)
                access_token = m.group()

        return access_token

    def get_category_info(self, token, blogname, output = 'json'):
        url = "https://www.tistory.com/apis/category/list"

        params = {
            'access_token' :  token,
            'output' : output,
            'blogName' : blogname
        }

        res = requests.get(url, params=params)

        return json.loads(res.text)['tistory']['item']['categories']

    def upload(self, args):
        url = 'https://www.tistory.com/apis/post/write'

        params = {
            'access_token': args[0],
            'output': args[1],
            'blogName': args[2],
            'title': args[3],
            'content': args[4],
            'visibility': args[5],
            'category': args[6],
            'tag': args[9],
            'acceptComment': args[10],
            'password': args[11]
        }

        res = requests.post(url, data = params)
        print(res)