
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from API.views import WatchListAV,WatchDetailAV,StreamPlatformVS,StreamDetailAV,\
    ReviewList,ReviewDetail,ReviewCreate


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')
urlpatterns = [
    path('list/',WatchListAV.as_view(),name='movie-list'),
    path('list/<int:pk>',WatchDetailAV.as_view(),name='movie-detail'),


    path('',include(router.urls)),
    path('stream/<int:pk>/review-create',ReviewCreate.as_view(),name='review-create'),
    path('stream/<int:pk>/review',ReviewList.as_view(),name='review-list'),
    path('stream/review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),




    # path('review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),
    # path('stream/',StreamPlatformAV.as_view(),name='stream'),
    # path('stream/<int:pk>',StreamDetailAV.as_view(),name='stream-detail'),
]