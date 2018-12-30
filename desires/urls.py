from django.urls import path

from .views import (
        DesireList,
        DesireDetail,
        DesireListView,
        DesireCreateView,
        DesireUpdateView,
        DesireDeleteView
        )


urlpatterns = [
    path('desire/user/<int:pk>/', DesireDetail, name='desire-detail'),
    path('desire/user/new/', DesireCreateView, name='desire-create'),
    path('desire/user/<int:pk>/update/', DesireUpdateView.as_view(), name='desire-update'),
    path('desire/user/<int:pk>/delete/', DesireDeleteView.as_view(), name='desire-delete'),
    path('desire/user/list/',DesireList , name='desire-list-from-user'),
    path('desire/',DesireListView,name='desire-list'),
]
