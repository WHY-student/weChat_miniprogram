import os
import time
import traceback

from apps.flask_pj.model import *
from datetime import datetime, date, timedelta

# root_dir = os.path.dirname(os.path.abspath('.'))
# print(root_dir)
# with open(root_dir + "\\getSpeech\\words.tsv", "r", encoding="utf-8") as f:
#     content = f.read()
#     datas = content.split("\n\n")[:-1]
#     for data in datas:
#         info = data.split("\t")
#         print(info)
#         word_writing = info[0]
#         word_symbol = info[2]
#         word_pronunciation = str(datas.index(data)) + word_writing + ".mp3"
#         word_explanation = info[1]
#         if word_explanation[-1:] == "\n":
#             word_explanation = word_explanation[:-1]
#         word_example = info[3] + info[4] + "\n" + info[5] + info[6]
#     print(len(datas))

# path='C:\\Users\\情若炎兮\\Desktop\\实习APP\\group1\\flask_app\\flask_pj\\apps\\static\\pronunciation\\'
#
# # 获取该目录下所有文件，存入列表中
# fileList = os.listdir(path)
#
# n = 0
# for i in fileList:
#     # 设置旧文件名（就是路径+文件名）
#     oldname = path + os.sep + fileList[n]  # os.sep添加系统分隔符
#     # 设置新文件名
#     newname = oldname.split('.')[0]+oldname.split('.')[1]+'.'+oldname.split('.')[2]
#
#     os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
#     print(oldname, '======>', newname)
#
#     n += 1
# print(n)
#     # word_id = db.UUIDField(primary_key=True, default=uuid.uuid4())
#     # writing = db.StringField(required=True, unique=True)
#     # symbol = db.StringField(required=True)
#     # pronunciation = db.StringField(required=True)
#     # explanation = db.StringField(required=True)
#     # example = db.StringField(required=True)
#

# day = date.today()
# now = datetime.now()
# delta = timedelta(days=-1)
# n_days_after = now + delta
# print(n_days_after.strftime('%Y-%m-%d %H:%M:%S'))

#
#
# abb = "123456"
# print(abb[:10])

# day = date.today()
# now = datetime.now()
# print(now)
# now = str(now).split(".")[0]
# data = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S')
# delta = timedelta(days=5)  # days可以为正负数，当为负数时，n_days_after 与n_days_forward 的值与正数时相反；
# n_days_after = now + delta  # 当前日期推迟n天之后的时间
# n_days_forward = now - delta  # 当前日期向前推n天的时间
# print(datetime.now().strftime("%Y-%m-%d"))
# print(("当前日期：{}").format(day))
# t1="{}".format(day)
# t2="2020-05-05"
# time1 = t1.split("-")
# time2 = t2.split("-")
# date1 = date(int(time1[0]), int(time1[1]), int(time1[2]))
# date2 = date(int(time2[0]), int(time2[1]), int(time2[2]))
# print(date1.__sub__(date2).days)


import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.request.AlipayTradeWapPayRequest import AlipayTradeWapPayRequest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')

# 实例化客户端
alipay_client_config = AlipayClientConfig()
alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
alipay_client_config.app_id = '2021000118663628'
alipay_client_config.app_private_key = 'MIIEpAIBAAKCAQEAgksxp7kXYKvTe8uv6pigikOHMAcK51KLoO/eYGvV3LdybvmBcsqQEXZ5MFZu81nrfDXpOfjWDojdeeko7fQnID21BpKk9zo3E7JQCAW5XtDIWhBO6l5mQEH8Xj8+sJqdvYbohzjf+8A/itE/nCJl7FvPQmTnnn4hcjwfd3JKIYN53Ldr/CUpV5LKO8eqrDVeij8NrwCq8t3jK5JJmKyk3aFF7MM5xNTmQ+1XI04ALwI4B6UhBVZoAPwI/udYFGW5qvHArsOfR1wpFHy4ttwggXsMxgyLR/zl0ucGXD1skypfCC36y1VVoFga0liCgl+EQHgifqbJJ62hHzSVmF1wXwIDAQABAoIBAEI6uK3Z7uEr1l9KBUzJcml1s+Uc31UAZ4tSAoaeqeH8ucVhPIS+JIdL4oRImzNF1OaZfMkEDMLsnS/X7f8uqSjBVSBXMFWfGNoBPJ8nUbe5hu4I9iQ6Ad3N7Nt3aIVawq3RQqdhqLEOYv5MKPpTnd2MOYk1Q2sUECpCF3ie9sGbmo03I8LVHfDM+T4mc4eVQcgAUsqj5OFnDeY7CR8iGz/3r7r5oD824vCqTqYS35aVuMZYp1/nR51Aa4I4rNoDdeyr0nbOclvABD04SupWueGxa4BxT+jIQT74IMQvDk6VwTdon2anxra6tNeU4dK8lMGgr/7M2mNaVcvPNnekdYkCgYEAttuH2jq0SHKCeZrWghpMbgKVO0NeogCNevkg4D1N3IRxalGaFjoOc1JTlgrGdbCo3ttEi4up8s6DT29F+C1Mzlq2dC/GY18VHtzz8/kzOSCYsuc/S+entimfPqbcdahZD1phrr8vtjUZw1ph+ySUnLhS85XqYUc3aAz8ak5mgmUCgYEAtmkrcV9gqGm3q/fJ/fk1iaklDiF4bwkLv+xZ+m1ZxO2aEAK1iU/HYK5B/iPaSNzgQBEjs0O43VYBXEWOZotwjkwDwrJ0SK96Iq7jhBWwzU8Ls2vJVVaiJ+HzvBY86XDqOf3P7vIAll7CpvjgMaeAQl7zsGZpmhBc0urhpSNxGXMCgYEAje0Ypa5Yzb5rPN2MTxEAb4Z7s7LXmaAaL+97r/CFJXp62Q2bLlNDcgjdLaERZrmGaOsBadouP3JAgwAX68elTKkl4kpOjkR3jSvsAVpTgqylOH66Jz0XdBEcM7GpfXz8GymIlex4qNDQPUtCr342BuoeIEgk0fpHq/AgXpaZg+0CgYA2G5w3VQNm8XT6HdZc779hxjqnpmYDCbvigklub2FheNlqRmNzB6csloQczqXBV0NtvafJVR1RCmH87OUApfwNOZ8j8atspCCmiRoT5Bs9y2S9JAvktH4FNpEGCdKnrEbOTOuRBVgHQrSasthN4lG5XlEK0lYgzRm7ttCYG5tA4QKBgQCf1O/3w8oZEdcEOtwDzUgzm9+oYJkvWs6KBR7lQKS6qmorMoeLgOmCjaMFrjHfNcserIOiVq49IMaqL8oBN/ZHg9HPGcIy1cak85nFDmPiOxuHE0l1gHhdX65wSqJsgiR/R0be3UFWXBZCj9AS077V74WliaAHpiz8DCt9PyjsYQ=='
alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAisN/asRZgbPrKDEWXAD6SdcfDOo0yFZ7QrNNVUppIzM08kudmZCLGUz9FEDlf/NHWbaMttC/XpWJNxlx6l0CRX+Wdg9GTRhFIBsDfee5Sjc0GXEl/gGmbdajT7T/FbjaUguynpRu0ENUIUv7tLbzNAFVP3Z5T3fdUITU7wohfmjeE1uYsCxj/8SVLyG19e8V2QcxP6VuhJs7Fcim34aLcV+tHl1oGu7OfynoLiw++xZYqTwa4aAPrmoM0HTh+CQYQnMO3IS8krlnOmRLyG95E/y/U47VoFflfRcOqubw820gg9CYi63q16mv3gmr5wP0PDldLtzS9w5P9AhkJn7e/QIDAQAB'
client = DefaultAlipayClient(alipay_client_config, logger)


def post_pay():
    # 构造请求参数对象
    model = AlipayTradeCreateModel()
    model.out_trade_no = "200010301"
    model.total_amount = "88.88"
    model.subject = "Iphone6 16G"
    model.quit_url = "www.hao123.com"
    model.product_code = "QUICK_WAP_PAY"
    # self._biz_content = None
    # self._version = "1.0"
    # self._terminal_type = None
    # self._terminal_info = None
    # self._prod_code = None
    # self._notify_url = None
    # self._return_url = None
    # self._udf_params = None
    # self._need_encrypt = False
    request = AlipayTradeWapPayRequest(biz_model=model)
    # request2 = AlipayTradeQueryRequest(biz_model=model)
    # 执行API调用
    try:
        response_content = client.page_execute(request)
        print(response_content)
    except Exception as e:
        print(traceback.format_exc())
    try:
        pass
        # response_content = client.execute(request2)
        # print(response_content)
    except Exception as e:
        print(traceback.format_exc())


def query_pay():
    # alipay_client_config = AlipayClientConfig()
    # alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    # alipay_client_config.app_id = '2021000118663628'
    # alipay_client_config.app_private_key = 'MIIEpAIBAAKCAQEAgksxp7kXYKvTe8uv6pigikOHMAcK51KLoO/eYGvV3LdybvmBcsqQEXZ5MFZu81nrfDXpOfjWDojdeeko7fQnID21BpKk9zo3E7JQCAW5XtDIWhBO6l5mQEH8Xj8+sJqdvYbohzjf+8A/itE/nCJl7FvPQmTnnn4hcjwfd3JKIYN53Ldr/CUpV5LKO8eqrDVeij8NrwCq8t3jK5JJmKyk3aFF7MM5xNTmQ+1XI04ALwI4B6UhBVZoAPwI/udYFGW5qvHArsOfR1wpFHy4ttwggXsMxgyLR/zl0ucGXD1skypfCC36y1VVoFga0liCgl+EQHgifqbJJ62hHzSVmF1wXwIDAQABAoIBAEI6uK3Z7uEr1l9KBUzJcml1s+Uc31UAZ4tSAoaeqeH8ucVhPIS+JIdL4oRImzNF1OaZfMkEDMLsnS/X7f8uqSjBVSBXMFWfGNoBPJ8nUbe5hu4I9iQ6Ad3N7Nt3aIVawq3RQqdhqLEOYv5MKPpTnd2MOYk1Q2sUECpCF3ie9sGbmo03I8LVHfDM+T4mc4eVQcgAUsqj5OFnDeY7CR8iGz/3r7r5oD824vCqTqYS35aVuMZYp1/nR51Aa4I4rNoDdeyr0nbOclvABD04SupWueGxa4BxT+jIQT74IMQvDk6VwTdon2anxra6tNeU4dK8lMGgr/7M2mNaVcvPNnekdYkCgYEAttuH2jq0SHKCeZrWghpMbgKVO0NeogCNevkg4D1N3IRxalGaFjoOc1JTlgrGdbCo3ttEi4up8s6DT29F+C1Mzlq2dC/GY18VHtzz8/kzOSCYsuc/S+entimfPqbcdahZD1phrr8vtjUZw1ph+ySUnLhS85XqYUc3aAz8ak5mgmUCgYEAtmkrcV9gqGm3q/fJ/fk1iaklDiF4bwkLv+xZ+m1ZxO2aEAK1iU/HYK5B/iPaSNzgQBEjs0O43VYBXEWOZotwjkwDwrJ0SK96Iq7jhBWwzU8Ls2vJVVaiJ+HzvBY86XDqOf3P7vIAll7CpvjgMaeAQl7zsGZpmhBc0urhpSNxGXMCgYEAje0Ypa5Yzb5rPN2MTxEAb4Z7s7LXmaAaL+97r/CFJXp62Q2bLlNDcgjdLaERZrmGaOsBadouP3JAgwAX68elTKkl4kpOjkR3jSvsAVpTgqylOH66Jz0XdBEcM7GpfXz8GymIlex4qNDQPUtCr342BuoeIEgk0fpHq/AgXpaZg+0CgYA2G5w3VQNm8XT6HdZc779hxjqnpmYDCbvigklub2FheNlqRmNzB6csloQczqXBV0NtvafJVR1RCmH87OUApfwNOZ8j8atspCCmiRoT5Bs9y2S9JAvktH4FNpEGCdKnrEbOTOuRBVgHQrSasthN4lG5XlEK0lYgzRm7ttCYG5tA4QKBgQCf1O/3w8oZEdcEOtwDzUgzm9+oYJkvWs6KBR7lQKS6qmorMoeLgOmCjaMFrjHfNcserIOiVq49IMaqL8oBN/ZHg9HPGcIy1cak85nFDmPiOxuHE0l1gHhdX65wSqJsgiR/R0be3UFWXBZCj9AS077V74WliaAHpiz8DCt9PyjsYQ=='
    # alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAisN/asRZgbPrKDEWXAD6SdcfDOo0yFZ7QrNNVUppIzM08kudmZCLGUz9FEDlf/NHWbaMttC/XpWJNxlx6l0CRX+Wdg9GTRhFIBsDfee5Sjc0GXEl/gGmbdajT7T/FbjaUguynpRu0ENUIUv7tLbzNAFVP3Z5T3fdUITU7wohfmjeE1uYsCxj/8SVLyG19e8V2QcxP6VuhJs7Fcim34aLcV+tHl1oGu7OfynoLiw++xZYqTwa4aAPrmoM0HTh+CQYQnMO3IS8krlnOmRLyG95E/y/U47VoFflfRcOqubw820gg9CYi63q16mv3gmr5wP0PDldLtzS9w5P9AhkJn7e/QIDAQAB'
    # client = DefaultAlipayClient(alipay_client_config, logger)
    # self._biz_content = None
    # self._version = "1.0"
    # self._terminal_type = None
    # self._terminal_info = None
    # self._prod_code = None
    # self._notify_url = None
    # self._return_url = None
    # self._udf_params = None
    # self._need_encrypt = False
    request2 = AlipayTradeQueryRequest()
    request2.biz_content = {"out_trade_no": "200010301"}
    # 执行API调用
    try:
        response_content = client.execute(request2)
        print(response_content)
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    # dir1 = r'test.html'
    # os.startfile(dir1)
    post_pay()
    # query_pay()
