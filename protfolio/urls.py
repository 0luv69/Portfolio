
from django.contrib import admin
from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('mujilover/', admin.site.urls),
    
    path('', views.home, name='home'),
    path('details/<slug:slug>/', views.home, name='project_detail'),
    path('seo/', views.seo, name='seo'),
    path('contact/', views.contact, name='contact'),
    
    # path('contact/messages/', views.contact_messages_view, name='contact_messages'),


    path('t0/', views.temp0, name='temp0'),
    path('t1/', views.temp1, name='temp1'),
    path('t2/', views.temp2, name='temp2'),
    path('t3/', views.temp3, name='temp3'),
    path('t4/', views.temp4, name='temp4'),

    path("api/", views.project_list_json, name="project_json"),
    # path('import-projects/', views.import_projects_json, name='import-projects'),




]


