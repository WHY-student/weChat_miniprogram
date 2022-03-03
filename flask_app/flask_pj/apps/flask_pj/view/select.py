from flask import Blueprint, jsonify, request

from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils.constants import METHODTYPE

select = Blueprint('select', __name__, url_prefix='/selectBook')


# 已测
@select.route('/getBooks', methods=[METHODTYPE.POST])
def api_get_all_books():
    try:
        book_infos = Book.get_list()
        books = []
        for book_info in book_infos:
            book_all_words_numbers = Word_Book_Correspond.get_list(book_id=book_info["_id"]["$uuid"])
            book_all_words_numbers = len(book_all_words_numbers)
            book_one = {"book_name": book_info["book_name"], "book_cover": book_info["cover"],
                        "words": book_all_words_numbers, "level": book_info["level"],
                        "category": book_info["category"], "book_id": book_info["_id"]["$uuid"]}
            books.append(book_one)
        return jsonify(books)
    except Exception as e:
        return jsonify({"msg": str(e)})


@select.route('/select', methods=[METHODTYPE.POST])
def api_select_book():
    user_id = request.values.get("user_id")
    book_id = request.values.get("book_id")
    try:
        try:
            book = Book.objects.get(pk=book_id)
        except:
            msg = "没有此书"
            return jsonify({"msg": msg})
        # 向表中插入该行，并设复习计划为0，学习计划为10
        try:
            old_plan = User_Book_Study_Plan.objects.get(user_id=user_id, is_studying=True)
            old_plan.update(set__is_studying=False)
            old_plan.save()
        except:
            pass
        try:
            plan = User_Book_Study_Plan(user_id=user_id, book_id=book, daily_learn=10, daily_review=0, is_studying=True)
            plan.save()
            msg = "成功"
        except:
            old_plan.update(set__is_studying=True)
            old_plan.save()
            msg = "不要重复操作"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})
