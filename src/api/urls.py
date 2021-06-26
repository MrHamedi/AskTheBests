from django.urls import path 
from .views import QuestionsList,QuestionDetailView 

urlpatterns = [
    path("",QuestionsList.as_view()),
    path("<int:pk>/",QuestionDetailView.as_view()),
]