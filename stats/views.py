from django.shortcuts import render

# Create your views here.
def stats_view(request):
    return render(request,"stats.html",{})
