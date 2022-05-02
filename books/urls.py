from django.urls import path

from . import views
from .views import book_detail_view

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', book_detail_view, name='book_detail'),
    path('new/', views.BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/edit', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete', views.BookDeleteView.as_view(), name='book_delete'),

]
