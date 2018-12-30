from django.urls import path

from .views import (
        EmailLandPage,
        EmailSentView,
        EmailSentDetail,
        EmailToSendCreation,
        )


urlpatterns = [
    path('EmailAdmin/', EmailLandPage, name='EmailAdmin-land-page'),
    path('EmailAdmin/<int:pk>/', EmailSentDetail, name='EmailAdmin-detail'),
    path('EmailAdmin/new/', EmailToSendCreation, name='EmailAdmin-create'),
    path('EmailAdmin/list/',EmailSentView , name='EmailAdmin-list'),
]
