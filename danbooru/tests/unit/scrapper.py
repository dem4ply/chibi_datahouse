from danbooru.scrapper import danbooru, Danbooru_post
from danbooru.tasks import debug_task
import datetime
import unittest
from unittest.mock import patch, Mock
from vcr_unittest import VCRTestCase

from chibi_requests import Chibi_url

#from catalog.models import Catalog_pulse, Catalog


class Test_scan_index( VCRTestCase ):
    def _get_vcr_kwargs( self, **kw ):
        kw[ 'ignore_hosts' ] = [ 'waifus', 'localhost' ]
        return kw

    def setUp( self ):
        super().setUp()
        self.post = Danbooru_post(
            'https://danbooru.donmai.us/posts/9072492' )

    def test_should_work( self, *args, **kw ):
        images = list( danbooru.images_sites )
        self.assertTrue( images )

    def test_images_site_should_be_a_list_of_posts( self, *args, **kw ):
        images = list( danbooru.images_sites )
        self.assertTrue( images )
        for image in images:
            self.assertIsInstance( image, Danbooru_post )

    def test_post_should_have_tags( self ):
        self.assertTrue( self.post.tags )
        self.assertIsInstance( self.post.tags, dict )
        self.assertIn( 'character', self.post.tags )
        self.assertIn( 'general', self.post.tags )
        self.assertIn( 'meta', self.post.tags )
        self.assertIn( 'copyrights', self.post.tags )

    def test_post_should_have_copyrights( self ):
        self.assertTrue( self.post.copyrights )
        self.assertIsInstance( self.post.copyrights, dict )

    def test_post_should_have_character( self ):
        self.assertTrue( self.post.character )
        self.assertIsInstance( self.post.character, dict )

    def test_post_should_have_general( self ):
        self.assertTrue( self.post.general )
        self.assertIsInstance( self.post.general, dict )

    def test_post_should_have_meta( self ):
        self.assertTrue( self.post.meta )
        self.assertIsInstance( self.post.meta, dict )

    def test_post_should_have_tittle( self ):
        self.assertTrue( self.post.title )
        self.assertIsInstance( self.post.title, str )

    def test_post_should_have_pk( self ):
        self.assertTrue( self.post.pk )
        self.assertIsInstance( self.post.pk, int )

    def test_post_should_have_post_at( self ):
        self.assertTrue( self.post.post_at )
        self.assertIsInstance( self.post.post_at, datetime.datetime )

    def test_post_should_have_source( self ):
        self.assertTrue( self.post.source )
        self.assertIsInstance( self.post.source, Chibi_url )
