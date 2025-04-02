from danbooru.scrapper import danbooru, Danbooru_post
from danbooru.tasks import debug_task
import datetime
import unittest
from unittest.mock import patch, Mock
from vcr_unittest import VCRTestCase

from chibi_requests import Chibi_url
from danbooru.serializers import Post as Post_serializer
from danbooru.models import Post as Post_model


class Test_serializer_post( VCRTestCase ):
    def _get_vcr_kwargs( self, **kw ):
        kw[ 'ignore_hosts' ] = [ 'waifus', 'localhost' ]
        return kw

    def setUp( self ):
        super().setUp()
        self.post = Danbooru_post(
            'https://danbooru.donmai.us/posts/9072492' )

    def test_should_work( self, *args, **kw ):
        serializer = Post_serializer( data=self.post.info )
        result = serializer.is_valid()
        self.assertTrue( result )

    def test_serializer_when_save_should_create_a_model( self, *args, **kw ):
        serializer = Post_serializer( data=self.post.info )
        serializer.is_valid( raise_exception=True )
        model = serializer.save()
        self.assertTrue( model )
        self.assertIsInstance( model, Post_model )

    def test_serializer_should_return_create_at( self, *args, **kw ):
        serializer = Post_serializer( data=self.post.info )
        serializer.is_valid( raise_exception=True )
        self.assertIn( 'create_at', serializer.validated_data )
        self.assertTrue( serializer.validated_data[ 'create_at' ] )
        date = datetime.datetime.fromisoformat( '2025-03-30T08:35:00+00:00' )
        self.assertEqual(
            serializer.validated_data[ 'create_at' ].isoformat(),
            date.isoformat() )
