# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views import static
import glob
import os
from django.conf import settings
import plistlib
import utils
import models_mongo as db
import pymongo


def init_dayone_entries(request):
    # todo replace
    db.init_db()
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
        db.save_entry({
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
    return render_to_response('entry_list.html', {'entries': db.get_entry()})


def all_tags(request):
    return render_to_response('tags.html', {'tags': [1, 2, 3]})


def search(request):
    text = request.GET.get('text', '')
    p = db.search_entries(text)
    return render_to_response('entry_list.html', {'entries': p})


def howto(request):
    return render_to_response('howto.html')


def all_days(request):
    return render_to_response('days.html', {'days': db.get_days()})


def index(request):
    pass
