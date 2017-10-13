# -*- coding: UTF-8 -*-
from goal.settings import *
import urllib.request
import urllib.parse
import json
from sql_help import *


class UrlRequest:
    appID = WEIXIN_APPID
    appSecret = WEIXIN_APPSECRET
    access_token = ''

    def __init__(self):
        mysql = MySQL()
        access_token = mysql.get_accecc_token()
        self.access_token = access_token

    def url_request(self, url, params=None):
        if params:
            req = urllib.request.Request(url, params)
        else:
            req = urllib.request.Request(url, params)
        res = urllib.request.urlopen(req)
        urlResp = json.loads(res.read())
        return urlResp

    def get_menu(self):
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={0}'.format(self.access_token)
        return self.url_request(url)

    def create_menu(self):
        menu = {
            "button": [
                {
                    "type": "view",
                    "name": "发起目标",
                    #"url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1e0129928b50b3e7&redirect_uri=http%3A%2F%2F182.61.21.208%2Fweixin%2Fcreate%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect"
                    "url": "http://182.61.21.208/weixin/create/"
                },
                {
                    "type": "view",
                    "name": "历史目标",
                    #"url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1e0129928b50b3e7&redirect_uri=http%3A%2F%2F182.61.21.208%2Fweixin%2Fhistory%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect"
                    "url": "http://182.61.21.208/weixin/history/"
                },
                {
                    "name": "更多",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "执行排行",
                            #"url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1e0129928b50b3e7&redirect_uri=http%3A%2F%2F182.61.21.208%2Fweixin%2Franking%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect"
                            "url": "http://182.61.21.208/weixin/ranking/"
                        },
                        {
                            "type": "view",
                            "name": "监督目标",
                            #"url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1e0129928b50b3e7&redirect_uri=http%3A%2F%2F182.61.21.208%2Fweixin%2Fothers%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect"
                            "url": "http://182.61.21.208/weixin/others/"
                        }
                    ]
                }]
        }
        data = json.dumps(menu, ensure_ascii=False)

        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}'.format(self.access_token)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('encoding', 'utf-8')
        res = urllib.request.urlopen(req, data.encode())
        urlResp = json.loads(res.read())


if __name__ == '__main__':
    url_request = UrlRequest()
    url_request.create_menu()


