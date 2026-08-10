from django.shortcuts import render

def campus_map(request):
    return render(request, 'campus/map.html')