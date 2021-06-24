
from API.models import WatchList,StreamPlatform,Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True,read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'



class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True)
    '''StringRelatedField'''
    # watchlist = serializers.StringRelatedField(many=True)
    '''PrimaryKeyRelatedField'''
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    '''HyperlinkedRelatedField'''
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )
    class Meta:
        model = StreamPlatform
        fields = '__all__'


'''HyperlinkedModelSerializer'''

# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     watchlist = WatchListSerializer(many=True, read_only=True)
#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'