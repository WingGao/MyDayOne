# coding=utf-8
__author__ = 'wing'
from pymongo import *
from bson.codec_options import CodecOptions
from django.conf import settings
import pytz

client = MongoClient(settings.MONGODB_URL)

db = client['dayone']

coll_entry = db['entry'].with_options(codec_options=CodecOptions(
    tz_aware=True,
    tzinfo=pytz.timezone(settings.TIME_ZONE)))

coll_day = db['day']

TAG_DAY = ['D', 'Dl']

TAG_DAY_CN = {
    'D': '普通',
    'Dl': '恋爱'
}


def init_db():
    if 'entry' not in db.collection_names():
        db.create_collection('entry')
    else:
        coll_entry.drop()
    if 'day' not in db.collection_names():
        db.create_collection('day')
    else:
        coll_day.drop()
    _create_indexs()


def _create_indexs():
    if 'entry' not in db.collection_names():
        db.create_collection('entry')
    indexs = {
        '_text': [('text', TEXT)],
        'unq_uuid': 'uuid',
        '_date': 'date'
    }
    for k, v in indexs.items():
        if k not in coll_entry.index_information():
            print 'create_index:', k
            coll_entry.create_index(v, name=k, unique=k.startswith('unq_'))


def get_entry():
    return coll_entry.find().sort('date', DESCENDING)


def search_entries(p):
    # for i in coll_entry.find({'$text': {'$search': p, '$language': 'none'}}):
    # for i in coll_entry.find({'text': {'$regex': p}}):
    return coll_entry.find({'text': {'$regex': p}}).sort('date', DESCENDING)


def save_entry(entry):
    coll_entry.insert_one(entry)
    _parse_tags(entry)


def _parse_tags(entry):
    for i in entry['tags']:
        t = i.split('-', 1)
        if len(t) == 2 and t[0] in TAG_DAY:
            coll_day.insert_one({
                'date': entry['date'],
                'name': t[1],
                'type': t[0],
                'entry_id': entry['_id']
            })
            print t[0], t[1]


def get_days():
    return coll_day.find({}).sort('date', DESCENDING)


if __name__ == '__main__':
    print search_entries(u'\u732b')
    p = coll_entry.find_one({'uuid': '0169E19A11D34A3BA01AFF1754E5DB42'})
    print p
