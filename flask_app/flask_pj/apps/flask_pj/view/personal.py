import requests
import json
from flask import Blueprint, jsonify, request, abort

from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils import jsonHelper, constants
from flask_pj.apps.utils.constants import METHODTYPE
from flask_pj.apps import *
import flask_pj.apps.utils.constants as constant

personal = Blueprint('personal', __name__, url_prefix='/personal')


# 已测
@personal.route('/getClockons', methods=[METHODTYPE.POST])
def getClockons():
    if request.method == METHODTYPE.GET:
        abort(405)
    try:
        user_id = request.values.get("user_id")
        status = User_Learn_Status.objects(user_id=user_id, is_clockin=True)
        status_count = status.count()
        user = User.get_one(user_id=user_id)
        if status_count == 0:
            return jsonify({"msg": "成功", "max_length": 0, "clockons": [], "is_remind": user["is_remind"],
                            "remind_time": user["remind_time"]})
        status = status.order_by('-clockons')
        status = jsonHelper.bsonCollectionToDict(status)
        clockons, max_length, length = [], 0, 0
        clockons.append(status[0]['clockons'])
        for i in range(len(status) - 1):
            clockons.append(status[i + 1]['clockons'])
            if constants.get_days(clockons[i], clockons[i + 1]) == 1:
                length += 1
            else:
                if length > max_length:
                    max_length = length
                length = 0
        if length > max_length:
            max_length = length
        if max_length != 0:
            max_length += 1
        if len(status) == 1:
            max_length = 1
        return jsonify({"msg": "成功", "max_length": max_length, "clockons": clockons, "is_remind": user["is_remind"],
                        "remind_time": user["remind_time"]})
    except Exception as e:
        return jsonify({"msg": str(e), "max_length": None, "clockons": None, "is_remind": None, "remind_time": None})


@personal.route('/clockin', methods=[METHODTYPE.POST])
def clockin():
    try:
        now = constants.get_nowTime()
        user_id = request.values.get("user_id")
        status = User_Learn_Status.objects(user_id=user_id, clockons=now)
        status_count = status.count()
        if status_count == 0:
            msg = "未达成学习目标"
        else:
            status = status.first()
            plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
            book_id = plan["book_id"]["$uuid"]
            word_amount = Word_Book_Correspond.objects(book_id=book_id).count()
            word_records = User_Book_Learn_Record.get_list(user_id=user_id, book_id=book_id, is_studying=True)
            word_learnt = len(word_records)
            if word_amount == word_learnt and status["learn_amount"] == 0:
                msg = "已学完全部新词"
            else:
                today_learn = 0
                for word_record in word_records:
                    if word_record["study_time"].split(" ")[0] == now:
                        today_learn += 1
                if today_learn == word_learnt and today_learn >= plan["daily_learn"]:
                    status.update(set__is_clockin=True)
                    status.save()
                    msg = "成功"
                else:
                    to_learn = plan["daily_learn"] + plan["daily_review"] - today_learn
                    if to_learn > 0:
                        msg = "未达成学习目标"
                    else:
                        if status["is_clockin"] == False:
                            status.update(set__is_clockin=True)
                            status.save()
                            msg = "成功"
                        else:
                            msg = "今日已打卡"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@personal.route('/share', methods=[METHODTYPE.POST])
def share():
    try:
        study_time = constants.get_nowTime()
        user_id = request.values.get("user_id")
        user_avatar = User.get_one(pk=user_id)["avatar"]
        clockin_amount = User_Learn_Status.objects(user_id=user_id, is_clockin=True).count()
        status = User_Learn_Status.get_one(user_id=user_id, clockons=study_time)
        today_learn = status["learn_amount"] + status["review_amount"]
        return jsonify(
            {"msg": "成功", "avatar": user_avatar, "today_learn": today_learn, "clockin_amount": clockin_amount})
    except Exception as e:
        return jsonify({"msg": str(e), "avatar": None, "today_learn": None, "clockin_amount": None})


def set_one_message(user_id):
    try:
        plan_book_info = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan_book_info["book_id"]["$uuid"]
        now = constant.get_nowTime()
        today_learn = 0
        word_record_list = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True)
        for word_record in word_record_list:
            if word_record["study_time"].split(" ")[0] == now:
                today_learn += 1
        word_record_list = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True)
        book_learned_words_numbers = word_record_list.count()
        plan_day = plan_book_info["today_status"].split(" ")[0]
        if plan_day != now:
            today_learn = 0
            today_review = 0
        else:
            today_learn = int(plan_book_info["today_status"].split(" ")[1])
            today_review = int(plan_book_info["today_status"].split(" ")[2])
        today_learn = plan_book_info["daily_learn"] - today_learn
        today_learn = today_learn if today_learn > 0 else 0
        today_need_review = plan_book_info["daily_review"] - today_review
        if today_need_review > today_learn + book_learned_words_numbers - today_review:
            today_need_review = today_learn + book_learned_words_numbers - today_review
        if today_need_review < 0:
            today_need_review = 0
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        }
        response = requests.get(url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid"
                                    "=wxfacc648774646439&secret=d1148882a0a2e922a4493c0dd1913102", headers=headers)
        access_token = response.json()["access_token"]
        if access_token:
            data = {
                # "access_token": access_token,
                "touser": user_id,
                "template_id": "bNEVQXRERG9H1mQxGf-ctuarD8FNPmt81eqhypD--L4",
                "page": "/pages/homepage/homepage",
                "data":
                    {
                        "number3":
                            {
                                "value": today_learn
                            },
                        "number4":
                            {
                                "value": today_need_review
                            }
                    },
            }
            print(data)
            data = json.dumps(data)
            headers = {
                'WebRequest.ContentType': "application/x-www-form-urlencoded",
            }
            message_response = requests.post(
                url="https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}".format(access_token),
                data=data, headers=headers)
            msg = "成功" if message_response.status_code == 200 else "发送失败"
        else:
            msg = "未能返回正确的access_token"
        print(msg)
    except Exception as e:
        print(str(e))


@personal.route('/sendMessage', methods=[METHODTYPE.POST])
def set_message():
    try:
        user_id = request.values.get("user_id")
        user = User.objects.get(user_id=user_id)
        remind_time = request.values.get("time")
        print(remind_time)
        action = int(request.values.get("action"))
        print(scheduler.get_jobs())
        if action == 1:
            scheduler.add_job(func=set_one_message, trigger="cron", id=user_id, args=[user_id],
                            day="*/1",
                            hour=int(remind_time.split(':')[0]),
                            minute=int(remind_time.split(':')[1]))
            try:
                scheduler.start()
            except:
                pass
            print("发送消息结束")
            user.update(set__is_remind=True)
            user.update(set__remind_time=remind_time)
            user.save()
        elif action == 2:
            try:
                scheduler.remove_job(id=user_id)
            except:
                pass
            user.update(set__is_remind=False)
            user.save()
        else:
            try:
                scheduler.remove_job(id=user_id)
            except:
                pass
            scheduler.add_job(func=set_one_message, trigger="cron", id=user_id, args=[user_id],
                            day="*/1",
                            hour=int(remind_time.split(':')[0]),
                            minute=int(remind_time.split(':')[1]))
            user.update(set__remind_time=remind_time)
            # scheduler.start()
            user.save()
        print(scheduler.get_jobs())
        return jsonify({"msg": "成功"})
    except Exception as e:
        return jsonify({"msg": str(e)})


@personal.route('/getTest', methods=[METHODTYPE.GET])
def getTest():
    status = User_Learn_Status.objects().order_by('-clockons')
    status = jsonHelper.bsonCollectionToDict(status)
    return jsonify({"res":status})

