from django.urls import path


from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('get/', views.get_request, name='get'),
    path('post/', views.post_request, name='post'),
    path('prof/', views.teacher_my_page, name='teacher_my_page'),
]