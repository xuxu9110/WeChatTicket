from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import User

import urllib.parse
import urllib.request
import http.cookiejar


class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, lzma, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'learn.tsinghua.edu.cn',
            'Origin': 'https://learn.tsinghua.edu.cn',
            'Referer': 'https://learn.tsinghua.edu.cn/index.jsp',
            'Upgrade - Insecure - Requests':'1',
            'User-Agent':'''Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36
            (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36 OPR/40.0.2308.62'''
        }

        url = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(pro)
        header = []
        for key, value in headers.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        postDict = {
            'userid': self.input['student_id'],
            'userpass': self.input['password'],
            'submit1': '登录'
        }
        postData = urllib.parse.urlencode(postDict).encode()
        op = opener.open(url, postData)
        data = op.read()

        if data.decode().find('window.alert(')!= -1:
            raise ValidateError('认证失败！')


    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()
