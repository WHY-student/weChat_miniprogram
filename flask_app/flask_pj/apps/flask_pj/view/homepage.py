import math

from flask import Blueprint, jsonify, request, abort

import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils.constants import METHODTYPE

homepage = Blueprint('homepage', __name__, url_prefix='/homepage')


# 已测
@homepage.route('/', methods=[METHODTYPE.POST])
def getHomepage():
    if request.method == METHODTYPE.GET:
        abort(405)
    try:
        # 和人相关 包括 当前学的书，总的学的天数，总学的单词
        user_id = request.values.get("user_id")
        plan_book_info = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        days = User_Learn_Status.objects(user_id=user_id).count()
        learned_words_numbers = User_Book_Learn_Record.objects(user_id=user_id, is_studying=True).count()
        book_id = plan_book_info["book_id"]["$uuid"]
        # 和当前书相关的
        book_info = Book.get_one(pk=book_id)
        word_record_list = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True)
        book_learned_words_numbers = word_record_list.count()
        book_all_words_numbers = Word_Book_Correspond.objects(book_id=book_id).count()
        now = constant.get_nowTime()
        left_words_numbers = book_all_words_numbers - book_learned_words_numbers
        left_days = math.ceil(left_words_numbers / plan_book_info["daily_learn"])
        # 计算今日要学 most important
        plan_day = plan_book_info["today_status"].split(" ")[0]
        if plan_day != now:
            today_learn = 0
            today_review = 0
        else:
            today_learn = int(plan_book_info["today_status"].split(" ")[1])
            today_review = int(plan_book_info["today_status"].split(" ")[2])

        to_learn = 0
        today_learn = plan_book_info["daily_learn"] - today_learn
        to_learn += today_learn if today_learn > 0 else 0
        today_need_review = plan_book_info["daily_review"] - today_review
        if today_need_review > today_learn + book_learned_words_numbers - today_review:
            today_need_review = today_learn + book_learned_words_numbers - today_review
        to_learn += today_need_review if today_need_review > 0 else 0
        # 读取是否是VIP
        now_user = User.get_one(pk=user_id)
        return jsonify({"msg": "成功", "days": days, "words": learned_words_numbers, "book_name": book_info["book_name"],
                        "book_cover": book_info["cover"], "to_learn": to_learn, "left_days": left_days,
                        "total": book_all_words_numbers, "learned": book_learned_words_numbers,
                        "is_vip": now_user['is_vip']})
    except Exception as e:
        return jsonify({"msg": str(e), "days": None, "words": None, "book_name": None, "book_cover": None,
                        "to_learn": None, "left_days": None, "total": None, "learned": None, "is_vip": None})
