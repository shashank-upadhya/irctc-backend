from django.urls import path
from .views import TrainSearchView, TrainCreateUpdateView

urlpatterns = [
    path('search/', TrainSearchView.as_view(), name='train-search'),
    path('', TrainCreateUpdateView.as_view(), name='train-create-update'),
]