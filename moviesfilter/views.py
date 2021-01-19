from django.shortcuts import render
from movies.models import Movie
from django.db.models import Q
import json
filter_category = None
# Create your views here.

def filter_view(request):
    global filter_category
    if filter_category is None:
        with open("data/unique_vals.txt",'r') as file1:
            filter_category = json.load(file1)
    movieitems = Movie.objects.filter(ranking__lte=30).order_by('ranking')
    if request.method == "GET":
        movieitems = Movie.objects.filter(ranking__lte=30).order_by('ranking')

    if request.method == "POST":
        print(dict(request.POST))
        movieitems = output(dict(request.POST))
    
    # movieitems = Movie.objects.filter(ranking__lte=30).order_by('ranking')
    # print(movieitems,len(movieitems))
    return render(request,"movie_filter.html",{'movieitems': movieitems, 'filter_category':filter_category})

def output(query_dict):
    q = Q()
    keys = ['movie_rating','movie_certification','yearrange','genre','language','country']

    if query_dict['yearrange'][0]!="":
        years = query_dict['yearrange'][0].split(",")
        print(years)
        if len(years)==2:
            q|= Q(year__range = (years[0],years[1]))
        else:
            q|=Q(year__exact=years[0])

    if 'movie_rating' in query_dict:
        for index,item in enumerate(query_dict['movie_rating']):
            if index==0 and q:
                q&= Q(rating__startswith=item)
            else:
                q|= Q(rating__startswith=item)

    if 'movie_certification' in query_dict:
        for index,item in enumerate(query_dict['movie_certification']):
            if index==0 and q:
                q&= Q(certification__exact=item)
            else:
                q|= Q(certification__exact=item)

    for key in ['genre','language']:
        if key not in query_dict:
            continue
        for index,item in enumerate(query_dict[key]):
            if index==0 and q:
                q&= Q(**{f"{key}__contains":item})
            else:
                q|= Q(**{f"{key}__contains":item})

    if q:
        return Movie.objects.filter(q)
    else:
        return Movie.objects.none()