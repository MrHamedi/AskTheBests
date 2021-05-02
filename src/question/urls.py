from django.urls import path 
from .views import HomePageView,QuestionDetailView

app_name="question"


urlpatterns = [
    path("question/<int:pk>/",QuestionDetailView.as_view(),name="questionDetail"),
    path("",HomePageView.as_view(),name="homepage"),
]