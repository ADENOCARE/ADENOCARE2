from django.contrib import admin
from django.urls import path,include 
from app1.views import index,register, symptom_checker, lung_analysis, community, home, share_story,account_view,logout_view,classify_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),  # Corrected
    path('symptom_checker/', symptom_checker, name='symptom_checker'),  # Corrected
    path('lung_analysis/', lung_analysis, name='lung_analysis'),  # Corrected
    path('community/', community, name='community'),  # Corrected
    path('accounts/', include('allauth.urls')),
    path('share/', share_story, name='share_story'),
     path("account/", account_view, name="account"),
    path("logout/", logout_view, name="logout"),
    path('classify/', classify_image, name='classify')
]
     

