from flask import Blueprint, jsonify, request, abort

from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils.constants import METHODTYPE

myPlan = Blueprint('myPlan', __name__, url_prefix='/myPlan')

# 已测
@myPlan.route('/getPlan', methods=[METHODTYPE.POST])
def getPlan():
    if request.method == METHODTYPE.GET:
        abort(405)
    try:
        user_id = request.values.get("user_id")
        plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan["book_id"]["$uuid"]
        book = Book.get_one(pk=book_id)
        total = Word_Book_Correspond.objects(book_id=book_id).count()
        return jsonify({"msg": "成功", "daily_learn": plan["daily_learn"], "daily_review": plan["daily_review"],
                        "book_cover": book["cover"], "book_name": book["book_name"], "total": total})
    except Exception as e:
        return jsonify({"msg": str(e), "daily_learn": None, "daily_review": None,
                        "book_cover": None, "book_name": None, "total": None})


@myPlan.route('/changePlan', methods=[METHODTYPE.POST])
def changePlan():
    if request.method == METHODTYPE.GET:
        abort(405)
    try:
        user_id = request.values.get("user_id")
        daily_learn = request.values.get("daily_learn")
        daily_review = request.values.get("daily_review")
        plan = User_Book_Study_Plan.objects.get(user_id=user_id, is_studying=True)
        plan.update(set__daily_learn=daily_learn)
        plan.update(set__daily_review=daily_review)
        plan.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})
