from django.urls import path
from about_us.apps import AboutUsConfig
from about_us.views import RestaurantPageView

app_name = AboutUsConfig.name

urlpatterns = [
    path('about/', RestaurantPageView.as_view(), name='about'),
]
