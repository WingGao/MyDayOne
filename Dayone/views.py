# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views import static
import glob
import os
from django.conf import settings
import plistlib
import utils
from models_mongo import coll_entry, create_indexs
import pymongo


def init_dayone_entries(request):
    create_indexs()
    coll_entry.remove({})
    for f in glob.glob(os.path.join(settings.DAYONE_PATH, 'entries', '*.doentry')):
        # print f
        pl = plistlib.readPlist(f)
        create_date = utils.get_entry_date(pl['Creation Date'], pl['Time Zone'])
        uuid = pl['UUID']
        text = pl['Entry Text']
        tags = []
        if hasattr(pl, 'Tags'):
            tags = pl['Tags']
            # print tags
        # print uuid, create_date
        coll_entry.insert_one({
            'uuid': uuid,
            'date': create_date,
            'text': text,
            'image': os.path.exists(os.path.join(settings.DAYONE_PATH, 'photos', uuid + '.jpg')),
            'tags': tags
        })
    return HttpResponse('init success')


def photo(request, uuid):
    fname = uuid + '.jpg'
    return static.serve(request, fname, os.path.join(settings.DAYONE_PATH, 'photos'), False)


def all_entries(request):
    return render_to_response('entry_list.html', {'entries': coll_entry.find().sort('date', pymongo.DESCENDING)})


def all_tags(request):
    return render_to_response('tags.html', {'tags': [1, 2, 3]})


def search(request):
    text = request.GET.get('text', '')
    p = coll_entry.find({'text': {'$regex': text}})
    return render_to_response('entry_list.html', {'entries': p.sort('date', pymongo.DESCENDING)})


def index(request):
    pass
