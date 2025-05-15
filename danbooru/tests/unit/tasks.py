from danbooru.tasks import (
    debug_task, scan_page, scan_post, should_scan_post,
)
import datetime
import unittest
from unittest.mock import patch, Mock
from vcr_unittest import VCRTestCase
from danbooru.models import Post as Post_model

#from catalog.models import Catalog_pulse, Catalog


class Test_scan_index( VCRTestCase ):
    def _get_vcr_kwargs( self, **kw ):
        kw[ 'ignore_hosts' ] = [ 'waifus', 'localhost' ]
        return kw

    #@patch( 'catalog.models.Catalog.get' )
    #def test_should_work( self, catalog_get ):
    def test_should_work( self, *args, **kw ):
        debug_task.delay()

    @patch( 'danbooru.tasks.scan_page' )
    @patch( 'danbooru.tasks.scan_post' )
    def test_scan_page_should_call_scan_post(
            self, scan_post_mock, scan_page_mock ):
        scan_page.delay()
        scan_post_mock.delay.assert_called()
        for call in scan_post_mock.delay.call_args_list:
            self.assertIn( 'https://danbooru.donmai.us/posts/', call[0][0] )

    @patch( 'danbooru.tasks.scan_page' )
    @patch( 'danbooru.tasks.scan_post' )
    def test_scan_page_should_call_page_two(
            self, scan_post_mock, scan_page_mock ):
        scan_page.delay()
        scan_page_mock.delay.assert_called_with(
            'https://danbooru.donmai.us/posts?page=2' )

    @patch( 'danbooru.models.Post.save' )
    def test_scan_post_should_save_post( self, post_save, *args, **kw ):
        url = 'https://danbooru.donmai.us/posts/9072492'
        scan_post( url )
        post_save.assert_called()

    def test_scan_post_should_return_the_post_id( self, *args, **kw ):
        url = 'https://danbooru.donmai.us/posts/9072492'
        post_id = scan_post( url )
        self.assertTrue( post_id )
        self.assertIsInstance( post_id, int )
        model = Post_model.get( id=post_id )
        self.assertTrue( model )
        self.assertEqual( model.pk, post_id )

    @patch( 'danbooru.tasks.scan_post' )
    def test_validate_post_should_run_when_is_not_in_ES(
            self, scan_post_mock, *args, **kw ):
        url = 'https://danbooru.donmai.us/posts/9072492'
        if Post_model.exists( id='9072492' ):
            model = Post_model.get( id='9072492' )
            model.delete()
            Post_model._index.flush()
        self.assertFalse( Post_model.exists( id='9072492' ) )
        should_scan_post( url )

        scan_post_mock.delay.assert_called_with( url )

    @patch( 'danbooru.tasks.scan_post' )
    def test_validate_post_should_not_run_when_is_in_ES(
            self, scan_post_mock, *args, **kw ):
        url = 'https://danbooru.donmai.us/posts/9072492'
        if not Post_model.exists( id='9072492' ):
            scan_post( url )
            Post_model._index.flush()
        self.assertTrue( Post_model.exists( id='9072492' ) )
        should_scan_post( url )
        Post_model._index.flush()

        scan_post_mock.delay.assert_not_called

    @patch( 'danbooru.tasks.scan_post' )
    def test_validate_post_with_params_should_run_when_is_not_in_ES(
            self, scan_post_mock, *args, **kw ):
        url = 'https://danbooru.donmai.us/posts/9103704?q=2koma'
        if Post_model.exists( id='9103704' ):
            model = Post_model.get( id='9103704' )
            model.delete()
            Post_model._index.flush()
        self.assertFalse( Post_model.exists( id='9103704' ) )
        should_scan_post( url )

        scan_post_mock.delay.assert_called_with( url )

    @patch( 'danbooru.tasks.scan_post' )
    def test_validate_post_with_params_should_not_run_when_is_in_ES(
            self, scan_post_mock, *args, **kw ):
        url = 'https://danbooru.donmai.us/posts/9103704?q=2koma'
        if not Post_model.exists( id='9103704' ):
            scan_post( url )
            Post_model._index.flush()
        self.assertTrue( Post_model.exists( id='9103704' ) )
        should_scan_post( url )
        Post_model._index.flush()

        scan_post_mock.delay.assert_not_called


