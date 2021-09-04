import os
import time
import requests
import json


# 配置信息
msg_config = {
    "sleep_time": 5,  # 每一次执行后等待时间
    "file_path": "",  # 绝对路径，包含文件名
    "ding_api_url": "",  # 钉钉推送地址
}


dingtalk_headers = {
    'Content-Type': "application/json; charset=utf-8"
}


class Logs(object):
    def __init__(self, logs_file):
        self.if_file(logs_file)
        self.logs_file = logs_file

    @staticmethod
    def if_file(logs_file):
        if not os.access(logs_file, os.F_OK):
            raise LogsError("File '%s' does not exist" % logs_file)
        if not os.access(logs_file, os.R_OK):
            raise LogsError("File '%s' not readable" % logs_file)
        if os.path.isdir(logs_file):
            raise LogsError("File '%s' is a directory" % logs_file)

    def read(self, s=1):
        with open(self.logs_file) as logs_file:
            logs_file.seek(0, 2)
            while True:
                curr = logs_file.tell()
                line = logs_file.read()
                if not line:
                    logs_file.seek(curr)
                    time.sleep(s)
                else:
                    dingtalk(line)


class LogsError(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


def dingtalk(ctt):
    api_url = msg_config['ding_api_url']
    content = '【发现慢查询】：' + ctt
    json_text = {
        "at": {
            "isAtAll": False
        },
        "text": {
            "content": content
        },
        "msgtype": "text"
    }
    requests.post(api_url, data=json.dumps(json_text), headers=dingtalk_headers)


if __name__ == '__main__':
    t = Logs(msg_config['file_path'])
    t.read(s=msg_config['sleep_time'])
