import json


def bsonToDict(bso):
    jso = bso.to_json()
    dic = json.loads(jso)
    del dic["_id"]
    return dic


def bsonToDict_withID(bso):
    jso = bso.to_json()
    dic = json.loads(jso)
    return dic


def bsonCollectionToDict(bsoCol):
    ls = []
    for bso in bsoCol:
        dic = bsonToDict(bso)
        ls.append(dic)
    return ls


def bsonCollectionToDict_withID(bsoCol):
    ls = []
    for bso in bsoCol:
        dic = bsonToDict_withID(bso)
        ls.append(dic)
    return ls
