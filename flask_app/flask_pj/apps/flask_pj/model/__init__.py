import uuid
import mongoengine
from uuid import UUID
from flask_pj.apps.utils import jsonHelper
from flask_mongoengine import MongoEngine

# 定义 MongoEngine
db = MongoEngine()
USER = UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
BOOK = UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')
WORD = UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8')


class User(db.Document):
    user_id = db.StringField(primary_key=True)
    user_name = db.StringField(required=True)
    avatar = db.StringField(required=True)
    remind_time = db.StringField(required=True, default="00:00")
    is_remind = db.BooleanField(required=True)
    is_vip = db.BooleanField(required=True, default=False)
    trade_no = db.StringField(required=True)

    @staticmethod
    def get_one(**kwargs):
        print(type(kwargs))
        return jsonHelper.bsonToDict_withID(User.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict_withID(User.objects(**kwargs))


class Book(db.Document):
    book_id = db.UUIDField(primary_key=True)
    book_name = db.StringField(required=True, unique=True)
    cover = db.StringField(required=True)
    level = db.StringField(required=True)
    category = db.StringField(required=True)

    def init(self, book_name, cover, level, category):
        self.book_id = uuid.uuid3(BOOK, book_name)
        self.book_name = book_name
        self.cover = cover
        self.level = level
        self.category = category
        return self

    @staticmethod
    def get_one(**kwargs):
        return jsonHelper.bsonToDict_withID(Book.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict_withID(Book.objects(**kwargs))


class Word(db.Document):
    word_id = db.UUIDField(primary_key=True)
    writing = db.StringField(required=True, unique=True)
    symbol = db.StringField(required=True)
    pronunciation = db.StringField(required=True)
    explanation = db.StringField(required=True)
    example = db.StringField(required=True)

    def init(self, writing, symbol, pronunciation, explanation, example):
        self.word_id = uuid.uuid3(WORD, writing)
        self.writing = writing
        self.symbol = symbol
        self.pronunciation = pronunciation
        self.explanation = explanation
        self.example = example
        return self

    @staticmethod
    def get_one(**kwargs):
        return jsonHelper.bsonToDict_withID(Word.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict_withID(Word.objects(**kwargs))


class Word_Book_Correspond(db.Document):
    book_id = db.ReferenceField(Book, reverse_delete_rule=mongoengine.CASCADE)
    word_id = db.ReferenceField(Word, reverse_delete_rule=mongoengine.CASCADE, unique_with='book_id')

    @staticmethod
    def get_one(**kwargs):
        return jsonHelper.bsonToDict(Word_Book_Correspond.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict(Word_Book_Correspond.objects(**kwargs))


class User_Learn_Status(db.Document):
    user_id = db.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    clockons = db.StringField(required=True, unique_with='user_id')
    is_clockin = db.BooleanField(required=True)
    learn_amount = db.IntField(required=True)
    review_amount = db.IntField(required=True)

    @staticmethod
    def get_one(**kwargs):
        return jsonHelper.bsonToDict(User_Learn_Status.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict(User_Learn_Status.objects(**kwargs))


class User_Book_Study_Plan(db.Document):
    user_id = db.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    book_id = db.ReferenceField(Book, reverse_delete_rule=mongoengine.CASCADE, unique_with='user_id')
    today_status = db.StringField(required=True, default="2021-01-01 0 0")
    is_studying = db.BooleanField(required=True)
    daily_learn = db.IntField(required=True)
    daily_review = db.IntField(required=True)

    @staticmethod
    def get_one(**kwargs):
        return jsonHelper.bsonToDict(User_Book_Study_Plan.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict(User_Book_Study_Plan.objects(**kwargs))


class User_Book_Learn_Record(db.Document):
    user_id = db.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    book_id = db.ReferenceField(Book, reverse_delete_rule=mongoengine.CASCADE)
    word_id = db.ReferenceField(Word, reverse_delete_rule=mongoengine.CASCADE, unique_with=['user_id', 'book_id'])
    is_incorrect = db.BooleanField(required=True)
    is_star = db.BooleanField(required=True)
    is_studying = db.BooleanField(required=True)
    study_time = db.StringField(required=True)

    @staticmethod
    def get_one(**kwargs):
        return jsonHelper.bsonToDict(User_Book_Learn_Record.objects.get(**kwargs))

    @staticmethod
    def get_list(**kwargs):
        return jsonHelper.bsonCollectionToDict(User_Book_Learn_Record.objects(**kwargs))
