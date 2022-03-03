from flask import Blueprint, jsonify, current_app, request, abort

from flask_pj.apps.utils.constants import METHODTYPE

api = Blueprint('api', __name__)


@api.route('/', methods=[METHODTYPE.GET, METHODTYPE.POST])
def api_index():
    current_app.logger.info(f'{request.method} api.index')
    if request.method == METHODTYPE.GET:
        data = request.args
        return jsonify({"success": True, "name": 'api.index', 'data': data})
    else:
        data = request.json  # for request that POST with application/json
        print("OK")
        return {"success": "OK"}
        # return jsonify({"success": True, "name": 'api.index', 'data': data})


@api.route('/upload', methods=[METHODTYPE.POST])
def api_upload():
    current_app.logger.info(f'{request.method} api.upload')
    if request.method == METHODTYPE.GET:
        abort(405)

    files = request.files  # for request that POST with multipart/form-data's files
    data = request.form  # for request that POST with multipart/form-data's data
    return jsonify({"success": True, "name": 'api.upload', 'data': data, 'files': files})

# @api.route('/homepage', methods=[METHODTYPE.POST])
# def api_get_homepage(user_id):
#     user_id = request.values.get("user_id")
#     current_app.logger.info(f'{request.method} api.upload')
#     if request.method == METHODTYPE.GET:
#         abort(405)
#
#     plan_book_info = get_plan_book_from_User_Book_Study_plan(user_id)
#     book_info = get_book_info_from_Book(plan_book_info["book_id"])
#     learn_Stauts = get_from_User_Learn_Status(user_id)
#     now = constant.get_nowTime()
#     days = constant.get_days(learn_Stauts["dockons"], now)
#     learned_words_numbers = get_learned_from_User_Book_Learn_Record(user_id, book_info["book_id"])
#     book_all_words_numbers = get_words_numbers_from_Word_Book_Correspond(book_info["book_id"])
#     # 这里需要一个今日已学单词数量
#     to_learn = learn_Stauts["learn_amount"]
#     left_days = math.ceil((book_all_words_numbers - learned_words_numbers) / int(plan_book_info["daily_learn"]))
#     return jsonify({"days": days, "words": learned_words_numbers, "book_name": book_info["book_name"],
#                     "book_cover": book_info["book_cover"], "to_learn": to_learn, "left_days": left_days})
#
#
# @api.route('/changeBook/getMyBooks', methods=[METHODTYPE.POST])
# def api_get_books(user_id):
#     book_ids = get_books_from_User_Book_Study_Plan(user_id)
#     books = []
#     for book_id in book_ids:
#         book_info = get_book_info_from_Book(book_id)
#         book_all_words_numbers = get_words_numbers_from_Word_Book_Correspond(book_id)
#         learned_words_numbers = get_learned_from_User_Book_Learn_Record(user_id, book_id)
#         to_learn = book_all_words_numbers - learned_words_numbers
#         book_one = jsonify({"book_cover": book_info["book_cover"], "book_name": book_info["book_name"],
#                             "words": book_all_words_numbers, "to_learn": to_learn})
#         books.append(book_one)
#     return books
#
#
# @api.route('/changeBook/deleteBook', methods=[METHODTYPE.POST])
# def api_delete_book(user_id, book_id):
#     # 这两个地方需要删除，并返回是否成功代码state
#     # delete_from_User_Book_Learn_Record(user_id,book_id)
#     # delete_from_User_Book_Study_Plan(user_id,book_id)
#     state = True
#     if state:
#         msg = "成功"
#     else:
#         msg = "没有此书"
#     return jsonify({"msg": msg})
#
#
# @api.route('/changeBook/clearProgress', methods=[METHODTYPE.POST])
# def api_clear_book(user_id, book_id):
#     # 需要清空，并返回是否成功代码state
#     # 这里利用前一个直接删除即可
#     # delete_from_User_Book_Learn_Record(user_id,book_id)
#     state = True
#     if state:
#         msg = "成功"
#     else:
#         msg = "没有此书"
#     return jsonify({"msg": msg})
#
#
# @api.route('/changeBook/clearProgress', methods=[METHODTYPE.POST])
# def api_change_book(user_id, book_id):
#     # 需要清空，并返回是否成功代码state
#     # 这里只需要改一下这个表的book_id即可
#     # delete_from_User_Book_Study_Plan(user_id,book_id)
#     state = True
#     if state:
#         msg = "成功"
#     else:
#         msg = "没有此书"
#     return jsonify({"msg": msg})
#
#
# @api.route('/selectBook/getBooks', methods=[METHODTYPE.POST])
# def api_get_all_books():
#     book_infos = get_books_info_from_Book()
#     books = []
#     for book_info in book_infos:
#         book_all_words_numbers = get_words_numbers_from_Word_Book_Correspond(book_info["book_id"])
#         book_one = jsonify({"book_name": book_info["book_name"], "book_cover": book_info["book_cover"],
#                             "words": book_all_words_numbers, "level": book_info["level"],
#                             "category": book_info["category"], "book_id": book_info["book_id"]})
#         books.append(book_one)
#     return books
#
#
# @api.route('/selectBook/select', methods=[METHODTYPE.POST])
# def api_select_book(user_id,book_id):
#     try:
#         # 向表中插入该行，并设复习计划为0，学习计划为10
#         addPlan_to_User_Book_Study_Plan(user_id,book_id)
#         msg = "成功"
#     except Exception as e:
#         msg = e
#     return msg
#
#
# @api.route('/practice/getWords', methods=[METHODTYPE.POST])
# def api_practice(user_id,source):
#     to_learn_words =
#
#
# @api.route('/practice/wrongWords', methods=[METHODTYPE.POST])
# def api_wrong_word(user_id,word_id,action):
#     if action == 1:
#         msg = record_to_change_incorrect(user_id,word_id,True)
#     elif action == 2:
#         msg = record_to_change_incorrect(user_id,word_id,False)
#     else:
#         msg = "action参数错误"
#     return msg
#
#
# @api.route('/practice/click', methods=[METHODTYPE.POST])
# def api_wrong_word(user_id,book_id,word_id):
#     msg = record_to_add(user_id,book_id,word_id,False)
#
#     return msg
#
#
#
# def get_plan_book_from_User_Book_Study_plan(user_id):
#     book_info = {
#         "book_id": "001",
#         "daily_learn": "10",
#         "daily_review": "10"
#     }
#     return book_info
#
#
# def get_book_info_from_Book(book_id):
#     book_info = {
#         "book_id": "001",
#         "book_name": "test",
#         "book_cover": "http://",
#         "level": "一年级",
#         "category": "人教版"
#     }
#     return book_info
#
#
# def get_from_User_Learn_Status(user_id):
#     user_learn_Status = {
#         "dockons": "2021-07-03 14:22:38",
#         "learn_amount": "10"
#     }
#     return user_learn_Status
#
#
# def get_learned_from_User_Book_Learn_Record(user_id, book_id):
#     numbers = 10
#     return numbers
#
#
# def get_words_numbers_from_Word_Book_Correspond(book_id):
#     numbers = 10
#     return numbers
#
#
# def get_books_from_User_Book_Study_Plan(user_id):
#     book_ids = ["001", "002"]
#     return book_ids
#
#
# def get_books_info_from_Book():
#     all_book_infos = [{}]
#     return all_book_infos
#
#
# def addPlan_to_User_Book_Study_Plan(user_id,book_id):
#     return True
#
#
# # 这里将User_Book_Learn_Record所有user_id,word_id匹配的单词的is_incorrect修改为传入的is_incorrect
# def record_to_change_incorrect(user_id,word_id,is_incorrect):
#     return "成功"
#
#
# # 向表中添加数据
# def record_to_add(user_id,book_id,word_id,is_incorrect):
#     return "成功"
#
#
