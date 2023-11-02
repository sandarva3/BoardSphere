from django.urls import path
from .views import(
    HomeView,
    BoardTopicsView,
    newTopic_view,
    PostView,
    #reply_view,
)
from boardapp import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('board/<int:pk>/', BoardTopicsView.as_view(), name='board_topics'),
    path('board/<int:pk>/new', newTopic_view, name='newtopic'),
    path('board/<int:pk>/topics/<int:topic_pk>/posts', PostView.as_view(), name='posts'),
    #path('board/<int:pk>/topics/<int:topic_pk>/reply', reply_view, name='reply'),
]