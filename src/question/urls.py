from django.urls import path 
from .views import HomePageView

app_name="question"


urlpatterns = [
    path("",HomePageView.as_view(),name="homepage"),
]