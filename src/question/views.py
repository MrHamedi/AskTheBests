from django.shortcuts import render
from .models import Question 
# Create your views here.
from django.views.generic import ListView 


#The view of the homepage  
class HomePageView(ListView):
    model=Question
    template_name="question/homepage.html"
    context_object_name="questions"
    paginate_by=1


