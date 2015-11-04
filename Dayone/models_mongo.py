# coding=utf-8
__author__ = 'wing'
from pymongo import *
from bson.codec_options import CodecOptions
from bson.dbref import DBRef
import bson.json_util
from django.conf import settings
import pytz

client = MongoClient(settings.MONGODB_URL)

db = client['dayone']
ENTRY_COLL_NAME = 'entry'
DAY_COLL_NAME = 'day'
TAG_COLL_NAME = 'tag'
coll_entry = db[ENTRY_COLL_NAME].with_options(codec_options=CodecOptions(
    tz_aware=True,
    tzinfo=pytz.timezone(settings.TIME_ZONE)))

coll_day = db[DAY_COLL_NAME]
coll_tag = db[TAG_COLL_NAME]

TAG_DAY = ['D', 'Dl']

TAG_DAY_CN = {
    'D': '普通',
    'Dl': '恋爱'
}


def init_db():
    for i in [ENTRY_COLL_NAME, DAY_COLL_NAME, TAG_COLL_NAME]:
        if i not in db.collection_names():
            db.create_collection(i)
        else:
            db[i].remove()
    _create_indexs()


def _create_indexs():
    indexs = {
        '_text': [('text', TEXT)],
        'unq_uuid': 'uuid',
        '_date': 'date'
    }
    for k, v in indexs.items():
        if k not in coll_entry.index_information():
            print 'create_index:', k
            coll_entry.create_index(v, name=k, unique=k.startswith('unq_'))


def get_entry(uuid=None):
    if uuid is not None:
        c = coll_entry.find({'uuid': uuid})
    else:
        c = coll_entry.find({})
    return c.sort('date', DESCENDING)


def get_entry_by_tag(tag):
    return [db.dereference(i) for i in coll_tag.find_one({'name': tag})['entries']]


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
                'uuid': entry['uuid']
            })
            print t[0], t[1]
        else:
            tag = coll_tag.find_one({'name': i})
            if tag is None:
                coll_tag.insert_one({
                    'name': i,
                    'entries': [DBRef(ENTRY_COLL_NAME, entry['_id'])]
                })
            else:
                coll_tag.update_one({'_id': tag['_id']},
                                    {'$push': {'entries': DBRef(ENTRY_COLL_NAME, entry['_id'])}})


def get_days():
    return coll_day.find({}).sort('date', DESCENDING)


def get_tags():
    return coll_tag.find({})


def dumps(d):
    return bson.json_util.dumps(d)


if __name__ == '__main__':
    print search_entries(u'\u732b')
    p = coll_entry.find_one({'uuid': '0169E19A11D34A3BA01AFF1754E5DB42'})
    print p
