from flask import Blueprint, jsonify, current_app, request, abort
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper
import requests
# 已测
login = Blueprint('login', __name__, url_prefix='/login')


@login.route('/', methods=[METHODTYPE.POST])
def get_login():
    print("request.values.get('user_id')", request.values.get("user_id"))
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=" + "wxfacc648774646439" + "&secret=" + \
          "d1148882a0a2e922a4493c0dd1913102" + "&js_code=" + \
          request.values.get("user_id") + "&grant_type=authorization_code"
    res = requests.get(url)
    print(res.json())
    # print(res.json()["openid"])
    # print("user_id", request.values.get("user_id"))
    if request.method == METHODTYPE.GET:
        abort(405)
    # user_id = request.values.get("user_id")
    user_id = res.json()["openid"]
    try:
        # user_id = request.values.get("user_id")
        try:
            test_user = User.objects.get(pk=user_id)
            print(test_user)
            msg = "数据库中已有该用户"
        except:
            user_name = request.values.get("user_name")
            avatar = request.values.get("avatar")
            user = User(user_id=user_id, user_name=user_name, avatar=avatar, is_remind=False,
                        remind_time="00:00", is_vip=False, trade_no="0")
            user.save()
            msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"user_id": user_id})
