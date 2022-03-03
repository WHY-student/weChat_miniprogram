from flask import Blueprint, jsonify, request, abort

from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils.constants import METHODTYPE
from flask_pj.apps.utils import constants, jsonHelper

words = Blueprint('words', __name__, url_prefix='/words')


# 已测
@words.route('/', methods=[METHODTYPE.POST])
def getWords():
    try:
        if request.method == METHODTYPE.GET:
            abort(405)
        user_id = request.values.get("user_id")
        plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan["book_id"]["$uuid"]
        all_words = Word_Book_Correspond.get_list(book_id=book_id)
        words_record = User_Book_Learn_Record.get_list(user_id=user_id, book_id=book_id, is_studying=True)
        not_learn_ids = []
        learn_ids = []
        for word in words_record:
            learn_ids.append(word["word_id"])
        for word in all_words:
            word_id = word["word_id"]
            if word_id not in learn_ids:
                not_learn_ids.append(word_id)
        not_learn_words = []
        for word_id in not_learn_ids:
            word_info = Word.get_one(pk=word_id["$uuid"])
            del word_info["_id"]
            word_info["word_id"] = word_id["$uuid"]
            del word_info["example"]
            not_learn_words.append(word_info)
        learn_words = []
        for i in range(0, len(learn_ids)):
            word_id = learn_ids[i]
            word_info = Word.get_one(pk=word_id["$uuid"])
            del word_info["_id"]
            word_info["word_id"] = word_id["$uuid"]
            del word_info["example"]
            word_info["is_in_wrongwords"] = words_record[i]["is_incorrect"]
            word_info["is_in_collection"] = words_record[i]["is_star"]
            learn_words.append(word_info)
        return jsonify({"msg": "成功", "not_learn": not_learn_words, "learn": learn_words})
    except Exception as e:
        return jsonify({"msg": str(e), "not_learn": None, "learn": None})


@words.route('/collection', methods=[METHODTYPE.POST])
def changeCollection():
    try:
        word_id = request.values.get("word_id")
        user_id = request.values.get("user_id")
        plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan["book_id"]["$uuid"]
        record = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, word_id=word_id)
        if record.count() == 0:
            detail_time = constants.get_delay_time(-1)
            book = Book.objects.get(book_id=book_id)
            word = Word.objects.get(word_id=word_id)
            record = User_Book_Learn_Record(user_id=user_id, book_id=book, word_id=word, is_incorrect=False,
                                            is_star=True, is_studying=False, study_time=detail_time)
            record.save()
        else:
            record = record.first()
            star = jsonHelper.bsonToDict(record)["is_star"]
            record.update(set__is_star=(not star))
            record.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@words.route('/getWords', methods=[METHODTYPE.POST])
def getWrongOrStarWords():
    try:
        source = int(request.values.get("source"))
        user_id = request.values.get("user_id")
        plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan["book_id"]["$uuid"]
        resultset = []
        if source == 1:
            records = User_Book_Learn_Record.get_list(user_id=user_id, book_id=book_id, is_incorrect=True)
            for record in records:
                word_id = record["word_id"]["$uuid"]
                word = Word.get_one(pk=word_id)
                del word["_id"]
                word["word_id"] = word_id
                del word["example"]
                word["is_in_wrongwords"] = record["is_incorrect"]
                word["is_in_collection"] = record["is_star"]
                resultset.append(word)
        else:
            records = User_Book_Learn_Record.get_list(user_id=user_id, book_id=book_id, is_star=True)
            for record in records:
                word_id = record["word_id"]["$uuid"]
                word = Word.get_one(pk=word_id)
                del word["_id"]
                word["word_id"] = word_id
                del word["example"]
                word["is_in_wrongwords"] = record["is_incorrect"]
                word["is_in_collection"] = record["is_star"]
                resultset.append(word)
        return jsonify({"msg": "成功", "words": resultset})
    except Exception as e:
        return jsonify({"msg": str(e), "words": None})
