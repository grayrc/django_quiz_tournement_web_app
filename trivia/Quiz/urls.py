from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('tournements_home', views.tournements_home, name='tournements_home'),
    path('create_tournement', views.create_tournement, name='create_tournement'),
    path('tournement/<int:id>', views.tournement, name='tournement'),
    path('add_user', views.add_user, name='add_user'),
    path('view_current', views.view_current, name='view_current'),
    path('game/<int:id>', views.game, name='game'),
    path('high_scores', views.high_scores, name='high_scores'),
    path('view_future', views.view_future, name='view_future')
]
