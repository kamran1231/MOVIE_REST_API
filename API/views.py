
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework.views import APIView
from .models import WatchList,StreamPlatform,Review
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from API.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    #Filter with username
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    #Filter with query parameters
    def get_queryset(self):
        username = self.request.query_params.get('username')

        return Review.objects.filter(review_user__username=username)




class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]


    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!!')

        if watchlist.number_of_ratiing == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_of_ratiing += 1
        watchlist.save()




        serializer.save(watchlist=watchlist,review_user=review_user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [AdminOrReadOnly]
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]



class StreamDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            platfrom = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platfrom)
        return Response(serializer.data)


    def put(self,request,pk):
        platfrom = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platfrom,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self,request,pk):
        platfrom = StreamPlatform.objects.get(pk=pk)
        platfrom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatchList(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    '''Django Filter'''
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    '''Search filter'''
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']

    '''Order filter'''
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']

class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(StreamPlatform)
#         return Response(serializer.data)


# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform,many=True)
#         return Response(serializer.data)
#
#     def post(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

