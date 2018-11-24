import time
import types
import json
from time import mktime
from datetime import datetime
from dateutil.parser import parser
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from urllib.request import urlopen
import MediaFileSync.checkFolder
from .models import Settings, radarrMovie, radarrMovieList, Profile, ProfileRadarr, ProfileSonarr, ProfileLidarr

def index(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/index.html")
    return HttpResponse(template.render(context, request))

def profiles(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    profile_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'profile_list': profile_list,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/profiles.html")
    return HttpResponse(template.render(context, request))

def settings(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/settings.html")
    return HttpResponse(template.render(context, request))

def donate(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/donate.html")
    return HttpResponse(template.render(context, request))

def movies(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    rML = radarrMovieList()
    rML.movielist.clear
    prList = ProfileRadarr.objects.filter(profile_id=prof.id)
    data = urlopen(system_settings.radarr_path + "/api/movie?apikey=" + system_settings.radarr_apikey).read()
    output = json.loads(data)
    cnt = 0
    monCnt = 0
    monSync = 0
    monNotSync = 0
    for var in output:
        cnt = cnt + 1
        rm = radarrMovie()
        rm.title = var['title']
        rm.r_id = var['id']
        try:
            rd = var['inCinemas'][:10] # + " " + var['inCinemas'][11:16]
            rm.releaseDate = rd
        except KeyError:
            pass
                    
        lr = datetime.fromtimestamp(mktime(time.strptime(prof.profile_lastRun, "%b %d %Y %I:%M%p")))
        
        mId = 0
        for pr in prList:
            if pr.radarr_id == var["id"]:
                rm.media_id = pr.id
                mId = pr.id
                prLr = datetime.fromtimestamp(mktime(time.strptime(pr.lastRun, "%b %d %Y %I:%M%p")))
        
        if rm.media_id > 0:
            rm.isMonitored = True
            monCnt = monCnt + 1        

        if var['hasFile']:
            rm.folderName = var["folderName"]
            rm.fileName =  var["movieFile"]["relativePath"]
            rm.size = var["movieFile"]["size"]
            plu = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
            rm.lastUpdt = plu
            lu = datetime.fromtimestamp(mktime(time.strptime(plu, "%Y-%m-%d %H:%M")))
            if mId > 0:
                if lu >  prLr:
                    rm.isNewer = True
                    monNotSync = monNotSync + 1
                else:
                    rm.isNewer = False
                    monSync = monSync + 1
            else:
                rm.isNewer = False      

        rm.rating = var["ratings"]["value"]

        try:
            rm.tmdbid = var["tmdbId"]
        except KeyError:
            pass
        
        try:
            rm.imdbid = var["imdbId"]
        except KeyError:
            pass
        
        rML.movielist.append(rm)
    rML.count = cnt
    rML.monitoredCount = monCnt
    rML.syncCount = monSync
    rML.notSyncCount = monNotSync

    context = {
        'system_settings': system_settings,
        'testitem': rML,
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/movies.html")
    return HttpResponse(template.render(context, request))

def shows(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=1)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/shows.html")
    return HttpResponse(template.render(context, request))

def music(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=1)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/music.html")
    return HttpResponse(template.render(context, request))