import json
import time

from flask import Blueprint, jsonify, request, abort
import traceback
from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils import jsonHelper
from flask_pj.apps.utils.constants import METHODTYPE
import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.request.AlipayTradeRefundRequest import AlipayTradeRefundRequest
from alipay.aop.api.request.AlipayTradeWapPayRequest import AlipayTradeWapPayRequest
import os

pay = Blueprint('pay', __name__, url_prefix='/pay')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )


@pay.route('/', methods=[METHODTYPE.POST])
def postPay():
    logger = logging.getLogger('')
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2021000118663628'
    alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAusEje5DOs/mkGgNX9XDHg8Khsd30MgyLUeLfQu0AGEJAGP1TSHThMWeA1HL/nTI1QN8vsgFmdMVKLcDaFc3E4ThwQ+oVUS8AAEY0rY3+JWfkQuzbD0FLK2SOaoRXUrO9epKS19fNWY7hfoEene7S8NQNky5PfVtnVJ5mapVpYpd3YnaJA4r0bGXFMPxPx8MyqBsHKNuNXXoa5TOFifNQQhYyRWrMkG8++rFlvxPzCf1JAhXgaFFESV7U3ACWsDUwAD7t9lqMCu02mvDzKMiN4AuIvqlifOnl0WPaaRFFLU27cqOs2X0vH6odg62AcqPoy/jWZPEpk84wET6QzpfETQIDAQABAoIBACHTJXgV7DpQttY3UNEVki1dLSgoCTifaQR10PYwMtox9aYRC+qNsNPf6UeRZJa2J0sOoXbeJg50RVEwIs/cKxKXxE2osh+4IYnrLVNZ6nQf8wnkGHEU5GaBmgHU4nQKNgFjVtFdNsZHyLO+8yqrvOz9m0/TDXao/XgoEGixkxrWAGkMvsTY+9wdwGM0eM9f+8RXa8CUO2FvWtoX43EFYa2C7G+ZBsb0vTgM25K1Z75XhmWiv1HOs09zMSlSYcYz33BUbOmx7aqr7a7HVm4pKjgruq3rMmkkyQczoY4C6anACWNrUzA37u75+p8elp7qJtN3AqwNwNOsZzu5Wqhy54kCgYEA97BvBruOb8P0nF7oRfoO1uRFv2QUVmGPe20kdFma5xicysSp2GJS20tRv5u0pK5GxddWcyWOwKa9FGtuqhShCZxlBg4XiKD+HjOE5Lh2A987RAU4ru+8v/4LIUjCngnTMJ5N9+12LXFqB9TwAA/SOdzFEap312ndaCYUUtXt5tsCgYEAwQVLyzq/5lUoo/KKI4PBfVv77STskdTSPv1/1E6mmPpx/IT+EQmAJ4oPpMRp0i5aD3Tp2Znu3/tY+LfsZUiu0IGHwIX8B1N4S/oZQZs/2pd7RrdUT+eaOtUDu6K79hpBJkvB36Jqqg5VRaq+7jc8tEqQPqUoFKrMWzfjPEAPRfcCgYBmXU91W9xBCp40ZfDewrqRSyQcNjNFg+p1myS+xS2EpqJeFqsPF4ugv98YLjSY/sGXECjVS8dUjVSFdOT2e7IWM8F4oChPuiFrv+UDVczISuDGetXzTncWbdqRte1gvTS/2hzlAwmdPEsS04kgrWk3qqrzYx1GNKVhXqN1nJ5GkwKBgC/1vOt2YZA9wKdb8G76oe0gGezGq/FgTA1St5xtHoAMWp4//VEGZ01rxI9QLmsHEWGdzy0+Tlhg/65tJNPVx3oPdUelAwZe+xkFv5jJlogd84eSreRcy7mqjA7nVITF6UI2uKl0lcRDY3S4BFD0cKTrkgO+zcK03aocrN2fnSvpAoGAEyAkHyk6E6hDYa2FCO1dYWWMO9gab+LgWI/sXP7MC/MWy4U9HamhBa+tvgaKEBCgQJCGH9RUaQodHefdJsbjNupBNxKIw2xFJKwT2sNWyGeWKs+F5kV5MxrXXlrrkEun4tynxjW4+9iLLdXoK/rH1AwOl31lejwUePhGqK4yfrk='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAisN/asRZgbPrKDEWXAD6SdcfDOo0yFZ7QrNNVUppIzM08kudmZCLGUz9FEDlf/NHWbaMttC/XpWJNxlx6l0CRX+Wdg9GTRhFIBsDfee5Sjc0GXEl/gGmbdajT7T/FbjaUguynpRu0ENUIUv7tLbzNAFVP3Z5T3fdUITU7wohfmjeE1uYsCxj/8SVLyG19e8V2QcxP6VuhJs7Fcim34aLcV+tHl1oGu7OfynoLiw++xZYqTwa4aAPrmoM0HTh+CQYQnMO3IS8krlnOmRLyG95E/y/U47VoFflfRcOqubw820gg9CYi63q16mv3gmr5wP0PDldLtzS9w5P9AhkJn7e/QIDAQAB'
    client = DefaultAlipayClient(alipay_client_config, logger)
    if request.method == METHODTYPE.GET:
        abort(405)
    user_id = request.values.get("user_id")
    model = AlipayTradeCreateModel()
    ts = int(time.time()/10)
    model.out_trade_no = user_id + str(ts)
    # 并修改数据库中no避免订单重复
    now_user = User.objects.get(user_id=user_id)
    now_user.update(set__trade_no=model.out_trade_no)
    now_user.save()
    model.total_amount = request.values.get("total_amount")
    # 加入中文时需要编码
    model.subject = request.values.get("subject")
    model.quit_url = "www.hao123.com"
    model.product_code = "QUICK_WAP_PAY"
    request1 = AlipayTradeWapPayRequest(biz_model=model)
    # 这里可以添加返回API来进行异步通知
    # request1.notify_url = "http://10.127.154.246:8888/pay/notice"
    # 执行API调用
    try:
        response_content = client.page_execute(request1)
        print(response_content)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"msg": str(e), "html": ""})
    res = response_content
    with open('test.html', 'w+') as f:
        f.seek(0)
        f.truncate()
        f.write(res)
    os.startfile(r'test.html')
    return jsonify({"msg": "success", "html": res})


@pay.route('/query', methods=[METHODTYPE.POST])
def query_pay():
    logger = logging.getLogger('')
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2021000118663628'
    alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAusEje5DOs/mkGgNX9XDHg8Khsd30MgyLUeLfQu0AGEJAGP1TSHThMWeA1HL/nTI1QN8vsgFmdMVKLcDaFc3E4ThwQ+oVUS8AAEY0rY3+JWfkQuzbD0FLK2SOaoRXUrO9epKS19fNWY7hfoEene7S8NQNky5PfVtnVJ5mapVpYpd3YnaJA4r0bGXFMPxPx8MyqBsHKNuNXXoa5TOFifNQQhYyRWrMkG8++rFlvxPzCf1JAhXgaFFESV7U3ACWsDUwAD7t9lqMCu02mvDzKMiN4AuIvqlifOnl0WPaaRFFLU27cqOs2X0vH6odg62AcqPoy/jWZPEpk84wET6QzpfETQIDAQABAoIBACHTJXgV7DpQttY3UNEVki1dLSgoCTifaQR10PYwMtox9aYRC+qNsNPf6UeRZJa2J0sOoXbeJg50RVEwIs/cKxKXxE2osh+4IYnrLVNZ6nQf8wnkGHEU5GaBmgHU4nQKNgFjVtFdNsZHyLO+8yqrvOz9m0/TDXao/XgoEGixkxrWAGkMvsTY+9wdwGM0eM9f+8RXa8CUO2FvWtoX43EFYa2C7G+ZBsb0vTgM25K1Z75XhmWiv1HOs09zMSlSYcYz33BUbOmx7aqr7a7HVm4pKjgruq3rMmkkyQczoY4C6anACWNrUzA37u75+p8elp7qJtN3AqwNwNOsZzu5Wqhy54kCgYEA97BvBruOb8P0nF7oRfoO1uRFv2QUVmGPe20kdFma5xicysSp2GJS20tRv5u0pK5GxddWcyWOwKa9FGtuqhShCZxlBg4XiKD+HjOE5Lh2A987RAU4ru+8v/4LIUjCngnTMJ5N9+12LXFqB9TwAA/SOdzFEap312ndaCYUUtXt5tsCgYEAwQVLyzq/5lUoo/KKI4PBfVv77STskdTSPv1/1E6mmPpx/IT+EQmAJ4oPpMRp0i5aD3Tp2Znu3/tY+LfsZUiu0IGHwIX8B1N4S/oZQZs/2pd7RrdUT+eaOtUDu6K79hpBJkvB36Jqqg5VRaq+7jc8tEqQPqUoFKrMWzfjPEAPRfcCgYBmXU91W9xBCp40ZfDewrqRSyQcNjNFg+p1myS+xS2EpqJeFqsPF4ugv98YLjSY/sGXECjVS8dUjVSFdOT2e7IWM8F4oChPuiFrv+UDVczISuDGetXzTncWbdqRte1gvTS/2hzlAwmdPEsS04kgrWk3qqrzYx1GNKVhXqN1nJ5GkwKBgC/1vOt2YZA9wKdb8G76oe0gGezGq/FgTA1St5xtHoAMWp4//VEGZ01rxI9QLmsHEWGdzy0+Tlhg/65tJNPVx3oPdUelAwZe+xkFv5jJlogd84eSreRcy7mqjA7nVITF6UI2uKl0lcRDY3S4BFD0cKTrkgO+zcK03aocrN2fnSvpAoGAEyAkHyk6E6hDYa2FCO1dYWWMO9gab+LgWI/sXP7MC/MWy4U9HamhBa+tvgaKEBCgQJCGH9RUaQodHefdJsbjNupBNxKIw2xFJKwT2sNWyGeWKs+F5kV5MxrXXlrrkEun4tynxjW4+9iLLdXoK/rH1AwOl31lejwUePhGqK4yfrk='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAisN/asRZgbPrKDEWXAD6SdcfDOo0yFZ7QrNNVUppIzM08kudmZCLGUz9FEDlf/NHWbaMttC/XpWJNxlx6l0CRX+Wdg9GTRhFIBsDfee5Sjc0GXEl/gGmbdajT7T/FbjaUguynpRu0ENUIUv7tLbzNAFVP3Z5T3fdUITU7wohfmjeE1uYsCxj/8SVLyG19e8V2QcxP6VuhJs7Fcim34aLcV+tHl1oGu7OfynoLiw++xZYqTwa4aAPrmoM0HTh+CQYQnMO3IS8krlnOmRLyG95E/y/U47VoFflfRcOqubw820gg9CYi63q16mv3gmr5wP0PDldLtzS9w5P9AhkJn7e/QIDAQAB'
    client = DefaultAlipayClient(alipay_client_config, logger)
    user_id = request.values.get("user_id")
    test_user = User.get_one(user_id=user_id)
    request2 = AlipayTradeQueryRequest()
    request2.biz_content = {"out_trade_no": test_user['trade_no']}
    # 执行API调用
    try:
        response_content = client.execute(request2)
        print(response_content)
        response_content_json = json.loads(response_content)
        if response_content_json['msg'] == "Success":
            test_user = User.objects.get(user_id=user_id)
            test_user.update(is_vip=True)
            test_user.save()
            return jsonify({"msg": "Success"})
        else:
            return jsonify({"msg": "未支付成功"})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"msg": str(e)})


@pay.route('/notice', methods=[METHODTYPE.POST, METHODTYPE.GET])
def notice_pay():
    print(request.values)


@pay.route('/refund', methods=[METHODTYPE.POST])
def refund_pay():
    logger = logging.getLogger('')
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2021000118663628'
    alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAusEje5DOs/mkGgNX9XDHg8Khsd30MgyLUeLfQu0AGEJAGP1TSHThMWeA1HL/nTI1QN8vsgFmdMVKLcDaFc3E4ThwQ+oVUS8AAEY0rY3+JWfkQuzbD0FLK2SOaoRXUrO9epKS19fNWY7hfoEene7S8NQNky5PfVtnVJ5mapVpYpd3YnaJA4r0bGXFMPxPx8MyqBsHKNuNXXoa5TOFifNQQhYyRWrMkG8++rFlvxPzCf1JAhXgaFFESV7U3ACWsDUwAD7t9lqMCu02mvDzKMiN4AuIvqlifOnl0WPaaRFFLU27cqOs2X0vH6odg62AcqPoy/jWZPEpk84wET6QzpfETQIDAQABAoIBACHTJXgV7DpQttY3UNEVki1dLSgoCTifaQR10PYwMtox9aYRC+qNsNPf6UeRZJa2J0sOoXbeJg50RVEwIs/cKxKXxE2osh+4IYnrLVNZ6nQf8wnkGHEU5GaBmgHU4nQKNgFjVtFdNsZHyLO+8yqrvOz9m0/TDXao/XgoEGixkxrWAGkMvsTY+9wdwGM0eM9f+8RXa8CUO2FvWtoX43EFYa2C7G+ZBsb0vTgM25K1Z75XhmWiv1HOs09zMSlSYcYz33BUbOmx7aqr7a7HVm4pKjgruq3rMmkkyQczoY4C6anACWNrUzA37u75+p8elp7qJtN3AqwNwNOsZzu5Wqhy54kCgYEA97BvBruOb8P0nF7oRfoO1uRFv2QUVmGPe20kdFma5xicysSp2GJS20tRv5u0pK5GxddWcyWOwKa9FGtuqhShCZxlBg4XiKD+HjOE5Lh2A987RAU4ru+8v/4LIUjCngnTMJ5N9+12LXFqB9TwAA/SOdzFEap312ndaCYUUtXt5tsCgYEAwQVLyzq/5lUoo/KKI4PBfVv77STskdTSPv1/1E6mmPpx/IT+EQmAJ4oPpMRp0i5aD3Tp2Znu3/tY+LfsZUiu0IGHwIX8B1N4S/oZQZs/2pd7RrdUT+eaOtUDu6K79hpBJkvB36Jqqg5VRaq+7jc8tEqQPqUoFKrMWzfjPEAPRfcCgYBmXU91W9xBCp40ZfDewrqRSyQcNjNFg+p1myS+xS2EpqJeFqsPF4ugv98YLjSY/sGXECjVS8dUjVSFdOT2e7IWM8F4oChPuiFrv+UDVczISuDGetXzTncWbdqRte1gvTS/2hzlAwmdPEsS04kgrWk3qqrzYx1GNKVhXqN1nJ5GkwKBgC/1vOt2YZA9wKdb8G76oe0gGezGq/FgTA1St5xtHoAMWp4//VEGZ01rxI9QLmsHEWGdzy0+Tlhg/65tJNPVx3oPdUelAwZe+xkFv5jJlogd84eSreRcy7mqjA7nVITF6UI2uKl0lcRDY3S4BFD0cKTrkgO+zcK03aocrN2fnSvpAoGAEyAkHyk6E6hDYa2FCO1dYWWMO9gab+LgWI/sXP7MC/MWy4U9HamhBa+tvgaKEBCgQJCGH9RUaQodHefdJsbjNupBNxKIw2xFJKwT2sNWyGeWKs+F5kV5MxrXXlrrkEun4tynxjW4+9iLLdXoK/rH1AwOl31lejwUePhGqK4yfrk='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAisN/asRZgbPrKDEWXAD6SdcfDOo0yFZ7QrNNVUppIzM08kudmZCLGUz9FEDlf/NHWbaMttC/XpWJNxlx6l0CRX+Wdg9GTRhFIBsDfee5Sjc0GXEl/gGmbdajT7T/FbjaUguynpRu0ENUIUv7tLbzNAFVP3Z5T3fdUITU7wohfmjeE1uYsCxj/8SVLyG19e8V2QcxP6VuhJs7Fcim34aLcV+tHl1oGu7OfynoLiw++xZYqTwa4aAPrmoM0HTh+CQYQnMO3IS8krlnOmRLyG95E/y/U47VoFflfRcOqubw820gg9CYi63q16mv3gmr5wP0PDldLtzS9w5P9AhkJn7e/QIDAQAB'
    client = DefaultAlipayClient(alipay_client_config, logger)
    user_id = request.values.get("user_id")
    test_user_json = User.get_one(user_id=user_id)
    trade_no = test_user_json['trade_no']
    if test_user_json['is_vip']:
        request1 = AlipayTradeRefundRequest()
        request1.biz_content = {"out_trade_no": trade_no, "refund_amount": 88.88}
        refund_response = client.execute(request1)
        print(refund_response)
        if json.loads(refund_response)['msg'] == "Success":
            test_user = User.objects.get(user_id=user_id)
            test_user.update(is_vip=False)
            test_user.save()
            return jsonify({"msg": "退款成功"})
        else:
            return jsonify({"msg": "异常，请稍后重试，或联系管理员"})
    else:
        return jsonify({"msg": "你还不是VIP"})
