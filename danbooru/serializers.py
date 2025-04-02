from .models import Post as Post_model
from rest_framework import serializers


class Tag( serializers.Serializer ):
    name = serializers.CharField()

    class Meta:
        model = dict


class Post( serializers.Serializer ):
    title = serializers.CharField()
    source = serializers.CharField()
    url = serializers.CharField()
    pk = serializers.IntegerField()
    create_at = serializers.DateTimeField()

    tags = Tag( many=True )
    artists = Tag( many=True )
    copyrights = Tag( many=True )
    characters = Tag( many=True )
    meta_tags = Tag( many=True )

    class Meta:
        model = Post_model

    def create( self, data, **kw ):
        model = self.Meta.model( **data )
        model.save()
        return model
