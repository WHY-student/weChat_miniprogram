import random

from flask import Blueprint, jsonify, current_app, request, abort
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper

practice = Blueprint('practice', __name__, url_prefix='/practice')


# 已测
@practice.route('/getWords', methods=[METHODTYPE.POST])
def api_practice():
    try:
        user_id = request.values.get("user_id")
        source = int(request.values.get("source"))
        user_plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = user_plan["book_id"]["$uuid"]
        all_words = Word_Book_Correspond.get_list(book_id=book_id)
        to_learn_words_id = get_to_learn_words_id_list(source, user_plan, user_id, book_id, all_words)
        # 根据id列表来获取词
        to_learn_words = []
        print(to_learn_words_id)
        for word_id in to_learn_words_id:
            word_info = Word.get_one(word_id=word_id)
            wrong_ids = [word_id]
            wrong_choices = []
            while True:
                if len(wrong_choices) == 3:
                    break
                wrong_id = random.choice(all_words)["word_id"]["$uuid"]
                if wrong_id in wrong_ids:
                    continue
                wrong_ids.append(wrong_id)
                wrong_word = Word.get_one(word_id=wrong_id)
                wrong_choices.append(wrong_word["explanation"])
            examples = word_info["example"].split("\n")
            examples = [[examples[0], examples[1]], [examples[2], examples[3]]]
            del word_info["example"]
            word_info["examples"] = examples
            try:
                words_record = User_Book_Learn_Record.get_one(user_id=user_id, book_id=book_id, word_id=word_id)
                word_info["is_in_wrongwords"] = words_record["is_incorrect"]
                word_info["is_in_collection"] = words_record["is_star"]
            except:
                word_info["is_in_wrongwords"] = False
                word_info["is_in_collection"] = False
            word_info["wrong_choices"] = wrong_choices
            word_info["word_id"] = word_id
            to_learn_words.append(word_info)
        return jsonify(to_learn_words)
    except Exception as e:
        return jsonify({"msg": str(e)})


@practice.route('/continue', methods=[METHODTYPE.POST])
def api_continuee():
    try:
        user_id = request.values.get("user_id")
        user_plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = user_plan["book_id"]["$uuid"]
        all_words = Word_Book_Correspond.get_list(book_id=book_id)
        all_words_id = []
        for words in all_words:
            all_words_id.append(words["word_id"]["$uuid"])
        try:
            words_record = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True)
            words_record = jsonHelper.bsonCollectionToDict(words_record)
            words_id_record = []
            for word_record in words_record:
                words_id_record.append(word_record["word_id"]["$uuid"])
        except:
            words_id_record = []
        total_size = 0
        to_learn_words_id = []
        # 获取每天学习的内容
        for word_id in all_words_id:
            # 判断size是否足够每天的计划
            if total_size >= 10:
                break
            if word_id in words_id_record:
                continue
            else:
                to_learn_words_id.append(word_id)
                total_size += 1
        # 根据id列表来获取词
        to_learn_words = []
        print(to_learn_words_id)
        for word_id in to_learn_words_id:
            word_info = Word.get_one(word_id=word_id)
            wrong_ids = [word_id]
            wrong_choices = []
            while True:
                if len(wrong_choices) == 3:
                    break
                wrong_id = random.choice(all_words)["word_id"]["$uuid"]
                if wrong_id in wrong_ids:
                    continue
                wrong_ids.append(wrong_id)
                wrong_word = Word.get_one(word_id=wrong_id)
                wrong_choices.append(wrong_word["explanation"])
            examples = word_info["example"].split("\n")
            examples = [[examples[0], examples[1]], [examples[2], examples[3]]]
            del word_info["example"]
            word_info["examples"] = examples
            try:
                words_record = User_Book_Learn_Record.get_one(user_id=user_id, book_id=book_id, word_id=word_id)
                word_info["is_in_wrongwords"] = words_record["is_incorrect"]
                word_info["is_in_collection"] = words_record["is_star"]
            except:
                word_info["is_in_wrongwords"] = False
                word_info["is_in_collection"] = False
            word_info["wrong_choices"] = wrong_choices
            word_info["word_id"] = word_id
            to_learn_words.append(word_info)
        return jsonify(to_learn_words)
    except Exception as e:
        return jsonify({"msg": str(e)})


@practice.route('/wrongWords', methods=[METHODTYPE.POST])
def api_wrong_word():
    user_id = request.values.get("user_id")
    word_id = request.values.get("word_id")
    action = int(request.values.get("action"))
    book_id = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)["book_id"]["$uuid"]
    print(book_id)
    try:
        # try:
        word_Record = User_Book_Learn_Record.objects.get(user_id=user_id, book_id=book_id, word_id=word_id)
        # except:
        #     word_Record = User_Book_Learn_Record(user_id=user_id, book_id=book_id, word_id=word_id, is_incorrect=False,
        #                                          is_star=False, study_time=now)
        #     word_Record.save()
        #     word_Record = User_Book_Learn_Record.objects.get(user_id=user_id, book_id=book_id, word_id=word_id)
        print(word_Record)
        if action == 1:
            word_Record.update(set__is_incorrect=True)
        elif action == 2:
            word_Record.update(set__is_incorrect=False)
        else:
            msg = "action参数错误"
            return msg
        word_Record.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@practice.route('/click', methods=[METHODTYPE.POST])
def api_click_word():
    user_id = request.values.get("user_id")
    word_id = request.values.get("word_id")
    try:
        # study_time = constant.get_review_time(2)
        study_time = constant.get_nowTime()
        detail_time = constant.get_detail_time()
        learn_plan = User_Book_Study_Plan.objects.get(user_id=user_id, is_studying=True)
        book_id = jsonHelper.bsonToDict(learn_plan)["book_id"]["$uuid"]
        now = constant.get_nowTime()
        plan_day = learn_plan["today_status"].split(" ")[0]
        today_learn = int(learn_plan["today_status"].split(" ")[1])
        today_review = int(learn_plan["today_status"].split(" ")[2])
        if plan_day != now:
            today_learn = 0
            today_review = 0
        test_status_count = User_Learn_Status.objects(user_id=user_id, clockons=study_time).count()
        if test_status_count == 0:
            status = User_Learn_Status(user_id=user_id, clockons=study_time, is_clockin=False, learn_amount=0,
                                       review_amount=0)
            status.save()
        status = User_Learn_Status.objects.get(user_id=user_id, clockons=study_time)
        status_dict = jsonHelper.bsonToDict_withID(status)
        word_count = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, word_id=word_id).count()
        if word_count == 0:
            book = Book.objects.get(pk=book_id)
            word = Word.objects.get(pk=word_id)
            detail_time = constant.get_delay_time(-1)
            word_Record = User_Book_Learn_Record(user_id=user_id, book_id=book, word_id=word, is_incorrect=False,
                                                 is_star=False, study_time=detail_time, is_studying=True)
            word_Record.save()
            today_learn += 1
            status.update(set__learn_amount=status_dict["learn_amount"] + 1)
        else:
            word_Record = User_Book_Learn_Record.objects.get(user_id=user_id, book_id=book_id, word_id=word_id)
            word_Record.update(set__study_time=detail_time)
            if word_Record["is_studying"]:
                word_Record.update(set__is_studying=True)
                word_Record.save()
                today_review += 1
                status.update(set__review_amount=status_dict["review_amount"] + 1)
            else:
                word_Record.save()
                today_learn += 1
                status.update(set__learn_amount=status_dict["learn_amount"] + 1)
        status.save()
        learn_plan.update(set__today_status="{} {} {}".format(now, today_learn, today_review))
        learn_plan.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


def get_to_learn_words_id_list(source, user_plan, user_id, book_id, all_words):
    all_words_id = []
    for words in all_words:
        all_words_id.append(words["word_id"]["$uuid"])
    now = constant.get_nowTime()
    if source == 1:
        plan_day = user_plan["today_status"].split(" ")[0]
        if plan_day != now:
            today_learn = 0
            today_review = 0
        else:
            today_learn = int(user_plan["today_status"].split(" ")[1])
            today_review = int(user_plan["today_status"].split(" ")[2])
        today_need_learn = user_plan["daily_learn"] - today_learn if today_learn < user_plan["daily_learn"] else 0
        today_need_review = user_plan["daily_review"] - today_review if today_review < user_plan["daily_review"] else 0
        words_id_record = []
        words_not_today_reviewed_ids = []
        try:
            words_record = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True).order_by(
                "study_time")
            words_record = jsonHelper.bsonCollectionToDict(words_record)
            for word_record in words_record:
                if word_record["study_time"].split(" ")[0] != now:
                    words_not_today_reviewed_ids.append(word_record["word_id"]["$uuid"])
                words_id_record.append(word_record["word_id"]["$uuid"])
        except:
            pass
        total_size = 0
        size = 0
        to_learn_words_id = []
        # 获取每天学习的内容
        for word_id in all_words_id:
            # 判断size是否足够每天的计划
            if size >= today_need_learn:
                break
            if word_id in words_id_record:
                continue
            else:
                to_learn_words_id.append(word_id)
                size += 1
                total_size += 1
                if total_size == 10:
                    return to_learn_words_id
        # 获取每天复习的内容
        size = 0
        for word_id in words_not_today_reviewed_ids:
            # 判断size是否足够每天的计划
            if size >= today_need_review:
                break
            # if word["study_time"].split(' ')[0] == now:
            #     continue
            to_learn_words_id.append(word_id)
            size += 1
            total_size += 1
            if total_size == 10:
                return to_learn_words_id
    elif source == 2:
        try:
            to_learn_words_id = []
            to_learn_words = User_Book_Learn_Record.objects(
                user_id=user_id, book_id=book_id, is_incorrect=True).order_by("study_time")
            to_learn_words = jsonHelper.bsonCollectionToDict(to_learn_words)
            to_learn_words = to_learn_words[:10]
            for learn_word in to_learn_words:
                to_learn_words_id.append(learn_word["word_id"]["$uuid"])
        except:
            to_learn_words_id = []
    else:
        try:
            to_learn_words_id = []
            to_learn_words = User_Book_Learn_Record.objects(
                user_id=user_id, book_id=book_id, is_studying=True).order_by("study_time")
            to_learn_words = jsonHelper.bsonCollectionToDict(to_learn_words)
            to_learn_words = to_learn_words[:10]
            for learn_word in to_learn_words:
                # if learn_word["study_time"].split(' ')[0] == now:
                #     continue
                to_learn_words_id.append(learn_word["word_id"]["$uuid"])
        except:
            to_learn_words_id = []
    return to_learn_words_id
