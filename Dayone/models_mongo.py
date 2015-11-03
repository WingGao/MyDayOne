# coding=utf-8
__author__ = 'wing'
from pymongo import MongoClient, TEXT

client = MongoClient('localhost')

db = client['dayone']

coll_entry = db['coll_entry']


def create_indexs():
    indexs = {
        '_text': [('text', TEXT)],
        'unq_uuid': 'uuid',
        '_date': 'date'
    }
    for k, v in indexs.items():
        if k not in coll_entry.index_information():
            print 'create_index:', k
            coll_entry.create_index(v, name=k, unique=k.startswith('unq_'))


def search_entries(p):
    # for i in coll_entry.find({'$text': {'$search': p, '$language': 'none'}}):
    # for i in coll_entry.find({'text': {'$regex': p}}):
    return coll_entry.find({'text': {'$regex': p}})


if __name__ == '__main__':
    create_indexs()
    print search_entries(u'\u732b')
    p = coll_entry.find_one({'uuid': '0169E19A11D34A3BA01AFF1754E5DB42'})
    print p
