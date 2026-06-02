from django.urls import path
from .views import PrecosView

urlpatterns = [
    path('precos/', PrecosView.as_view(), name='precos'),
]
