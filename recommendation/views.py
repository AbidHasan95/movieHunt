from django.shortcuts import render
from movies.models import Movie
from django.db.models import Q
import json
import numpy as np
filter_category = None
movies_data = None

def recommendation_view(request):
    global filter_category
    if filter_category is None:
        with open("data/unique_vals.txt",'r') as file1:
            filter_category = json.load(file1)
    movieitems = Movie.objects.filter(ranking__lte=30).order_by('ranking')
    if request.method == "GET":
        movieitems = Movie.objects.filter(ranking__lte=30).order_by('ranking')

    if request.method == "POST":
        print(dict(request.POST))
        if "focusRankingsInput" in request.POST:
            movieitems = similar_movies(request.POST["focusRankingsInput"])
        else:
            movieitems = apply_filter(dict(request.POST))
    
    # movieitems = Movie.objects.filter(ranking__lte=30).order_by('ranking')
    # print(movieitems,len(movieitems))
    return render(request,"movie_filter_recommendation.html",{'movieitems': movieitems, 'filter_category':filter_category})

def apply_filter(query_dict):
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
        return Movie.objects.filter(q).order_by('ranking')
    else:
        return Movie.objects.none()

def similar_movies(movieRankings):
    print(movieRankings.split(", "),type(movieRankings))
    focusRankings = movieRankings.split(", ")
    output = closest_indices(focusRankings)
    return output
    

    
def closest_indices(indices):
    global movies_data
    if movies_data is None:
        movies_data = np.load("data/movies_feature_matrix.npy")
    a= 0
    print("indices",indices)
    for index in indices:
        print("index",index)
        a+=movies_data[int(index)-1]
    # a = movies_data[index-1]
    res = np.dot(a,movies_data.T)/(np.sqrt(np.dot(a,a.T)) * (np.sqrt(np.dot(movies_data,movies_data.T).diagonal())))
    res = np.argsort(res)
    res = res[::-1][:100]
    # print(res)
    res+=1
    res = res.tolist()
    out = Movie.objects.filter(ranking__in=res).order_by("ranking")
    res = np.argsort(res)
    out = zip(out,res)
    out = [i for i in out]
    out.sort(key = lambda x: x[1])
    out = [i[0] for i in out]
    return out




