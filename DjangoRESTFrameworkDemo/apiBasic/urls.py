from django.urls import path
from .views import article_list , article_detail, ArticleAPIView, ArticleViewSet, ArticleDetails, GenericAPIView
from rest_framework.routers import DefaultRouter
from django.conf.urls import include

router = DefaultRouter() 
router.register('article', ArticleViewSet, basename='article') #el parametro basename es un alias 

urlpatterns = [
    path('viewset/', include(router.urls)), # El path name puede ser cualquiera   
    path('viewset/<int:pk>/', include(router.urls)),  
    #path('viewset/article/<int:pk>/', include(router.urls)),  
    #path('article/',  article_list),
    path('article/',  ArticleAPIView.as_view()),
    #path('detail/<int:pk>/',  article_detail),
    path('detail/',  ArticleDetails.as_view()),
    path('generic/article/<int:id>/',  GenericAPIView.as_view()),
    
]
