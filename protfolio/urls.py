
from django.contrib import admin
from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('mujilover/', admin.site.urls),
    
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('seo/', views.seo, name='seo'),
    path('contact/', views.contact, name='contact'),
    
    # path('contact/messages/', views.contact_messages_view, name='contact_messages'),


    path('old/', views.old_portfolio, name='old-portfolio'),

    # path("api/", views.project_list_json, name="project_json"),
    # path('import-projects/', views.import_projects_json, name='import-projects'),




]


print("DEBUG MODE: Serving media files from MEDIA_URL", settings.DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)