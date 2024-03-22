from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models

class RecipeListView(ListView):
        
    model = models.Recipe
    template_name='recipes/home.html'
    context_object_name='recipes'




class RecipeDetailView(DetailView):
    model=models.Recipe