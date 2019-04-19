from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('restrict/', views.restict, name='restrict'),
    path('sql/<str:query>/', views.sql, name='sql'),
    path('xml/', views.xml, name='xml'),
    path('xml_upload/', views.xml_upload, name='xml_upload'),
    path('xss/', views.xss, name='xss'),
    path('xss_upload/', views.xss_upload, name='xss_upload'),
    path('serial/', views.serial, name='serial'),
    path('serial_download/', views.serial_download, name='serial_download'),
    path('serial_upload/', views.serial_upload, name='serial_upload'),
]