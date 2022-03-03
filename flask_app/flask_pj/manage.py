import os
import sys


def init_env_path(_file_):
    package_dir = os.path.join(os.path.dirname(_file_), '../')
    abs_path = os.path.abspath(package_dir)
    if abs_path not in sys.path:
        print(f'Add {abs_path} to python path')
        sys.path.insert(0, abs_path)


init_env_path(__file__)

from apps.utils import parse_args
from apps import create_app

__all__ = ['main']


def main():
    app = create_app()
    args = parse_args()
    # root_dir = os.path.dirname(os.path.abspath('.'))
    # print(root_dir)
    # with open(root_dir + "\\flask_pj\\apps\\static\\books.csv", "r", encoding="gb2312") as f:
    #     for line in f.readlines():
    #         line = line.strip('\n').split(',')
    #         book_name = line[0]
    #         cover = line[1]
    #         level = line[2]
    #         category = line[3]
    #         book = Book().init(book_name, cover, level, category)
    #         book.save()
    # for i in range(11):
    #     try:
    #         words = Word.objects()
    #         book = Book.objects[i]
    #         for word in words:
    #             correspond = Word_Book_Correspond()
    #             correspond.word_id = word
    #             correspond.book_id = book
    #             correspond.save()
    #     except:
    #         continue
    # user = User().init("1234ggggg", "x64b12345")
    # user.save()
    # user = User.objects.get(user_name="User1")
    # book = Book.objects.get(book_name="剑桥少儿英语")
    # plan = User_Book_Study_Plan(daily_learn=10, daily_review=10, is_studying=True)
    # plan.user_id = user
    # plan.book_id = book
    # plan.save()
    # print(list(books))
    # print('find_user',user)
    # print("user_id:", user_id)
    # root_dir = os.path.dirname(os.path.abspath('.'))
    # print(root_dir)
    # with open(root_dir + "\\flask_pj\\apps\\static\\words.tsv", "r", encoding="utf-8") as f:
    #     content = f.read()
    #     datas = content.split("\n\n")[:-1]
    #     for data in datas:
    #         info = data.split("\t")
    #         print(info)
    #         word_writing = info[0]
    #         word_symbol = info[2]
    #         word_pronunciation = "/pronunciation/" + str(datas.index(data)) + word_writing + ".mp3"
    #         word_explanation = info[1]
    #         if word_explanation[-1:] == "\n":
    #             word_explanation = word_explanation[:-1]
    #         word_example = info[3] + "\n" + info[4] + "\n" + info[5] + "\n" + info[6]
    #         word = Word.objects.get(writing=word_writing)
    #         word.update(set__example=word_example)
    #         word.save()
    #     print(len(datas))
    if args.cmd.isdigit():
        cmd = 'runserver'
        port = int(args.cmd)
    else:
        cmd = args.cmd
        port = args.port if args.port else 8080

    if cmd == 'runserver':
        app.run('0.0.0.0', port)
        app.logger.info(f'run server at port {port}')
    else:
        print('run command error')


if __name__ == '__main__':
    main()
