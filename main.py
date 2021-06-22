import web
import hashlib
# import receive
# import replay
from handle import Handle

urls = (
    '/wx', 'Handle',
)

'''
# 改get请求用于验证Token
class Handle(object):
    def GET(self):
        return " hello 测试成功"
    def GET(self):
        try:
            data = web.input()
            print(data)
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "KarmaLK" #请按照公众平台官网\基本配置中信息填写

            li = [token, timestamp, nonce]
            li.sort()
            tmp_str = "".join(li).encode('utf-8')
            #进行sha1加密
            hashcode = hashlib.sha1(tmp_str).hexdigest()

            #sha1 = hashlib.sha1()
            #map(sha1.update, li)
            #hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument
'''

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
