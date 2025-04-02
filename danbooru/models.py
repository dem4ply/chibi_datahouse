import datetime
from django.db import models

from chibi_django.models import ES_document
from chibi_django.snippet.elasticsearch import build_index_name
from chibi_django.snippet.elasticsearch import name, name_space
from elasticsearch_dsl import field, InnerDoc


class Tag( InnerDoc ):
    name = field.Text(
        analyzer=name, multi=True,
        fields={
            'space': field.Text( analyzer=name_space, multi=True ),
            'keyword': field.Keyword( multi=True ),
        } )


class Post( ES_document ):
    title = field.Text(
        analyzer=name, multi=True,
        fields={
            'space': field.Text( analyzer=name_space, multi=True ),
            'keyword': field.Keyword( multi=True ),
        } )
    source = field.Keyword()
    url = field.Keyword()
    pk = field.Integer()
    create_at = field.Date()

    tags = field.Nested( Tag )
    artists = field.Nested( Tag )
    copyrights = field.Nested( Tag )
    characters = field.Nested( Tag )
    meta = field.Nested( Tag )

    class Index:
        name = build_index_name( 'danbooru__post' )
        settings = { 'number_of_shards': 2, 'number_of_replicas': 1 }

    def save( self, *args, **kw ):
        if not getattr( self.meta, 'id', False ):
            if getattr( self, 'pk', False ):
                self.meta.id = str( self.pk )
            # el create_at debe de venir de los posts
            if not self.create_at:
                self.create_at = datetime.datetime.utcnow()
        self.update_at = datetime.datetime.utcnow()
        return super().save( *args, **kw )
