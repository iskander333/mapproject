# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search
from .forms import SearchForm
import folium
import geocoder
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save() 
            redirect('/')
    else:
        form = SearchForm()    
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('Your address input is invalid')
    # Create Map Object  
    m = folium.Map(location=[19, -12], zoom_start=2)
   
    folium.Marker([lat, lng], tooltip='Click for more',
    popup=country).add_to(m)
    # Get HTML Representaton of Map object
    m=m._repr_html_()    

    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)
