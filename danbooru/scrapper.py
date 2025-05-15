import datetime
from chibi_requests import Chibi_url
from chibi_site import Chibi_site


class Danbooru( Chibi_site ):
    @property
    def images_sites( self ):
        for article in self.articles:
            site = self + article.a.attrs[ 'href' ]
            yield Danbooru_post( site )
        """
        html_file = self.articles.to_html( to_temp=True )
        html_file.open_on_browser()
        import pdb
        pdb.set_trace()
        html_file = self.images.to_html( to_temp=True )
        html_file.open_on_browser()
        import pdb
        pdb.set_trace()
        pass
        """

    @property
    def next_page( self ):
        page_url = self.soup.select_one( '.paginator-next' ).attrs[ 'href' ]
        return self + page_url


class Danbooru_post( Chibi_site ):
    @property
    def info( self ):
        result = {
            'title': self.title,
            'pk': self.pk,
            'create_at': self.post_at.isoformat(),
            'source': self.source,

            'tags': [ { 'name': t } for t in self.general ],
            'artists': [ { 'name': t } for t in self.artists ],
            'copyrights': [ { 'name': t } for t in self.copyrights ],
            'characters': [ { 'name': t } for t in self.character ],
            'meta_tags': [ { 'name': t } for t in self.meta ],
            'url': str( self )
        }
        return result

    @property
    def tags( self ):
        return {
            'artist': self.artists,
            'copyrights': self.copyrights,
            'character': self.character,
            'general': self.general,
            'meta': self.meta,
        }

    @property
    def artists( self ):
        return self.get_tags( 'artist' )

    @property
    def copyrights( self ):
        return self.get_tags( 'copyright' )

    @property
    def character( self ):
        return self.get_tags( 'character' )

    @property
    def general( self ):
        return self.get_tags( 'general' )

    @property
    def meta( self ):
        return self.get_tags( 'meta' )

    @property
    def title( self ):
        image = self.soup.select_one( 'img#image' )
        if image is None:
            title, trash = self.soup.title.text.rsplit( '|' )
            return title.strip()
        return image.attrs[ 'alt' ]

    @property
    def pk( self ):
        info = self.soup.select_one( 'li#post-info-id' )
        return int( info.text.split( ':' )[1].strip() )

    @property
    def post_at( self ):
        info = self.soup.select_one( 'li#post-info-date time' )
        result = datetime.datetime.fromisoformat( info.attrs[ 'datetime' ] )
        return result

    @property
    def source( self ):
        info = self.soup.select_one( 'li#post-info-source a' )
        if info is None:
            info = self.soup.select_one( 'li#post-info-source' )
            return info.text
        return Chibi_url( info.attrs[ 'href' ] )

    def get_tags( self, name ):
        tags = self.soup.select_one( '#tag-list' )
        links = tags.select( f'ul.{name}-tag-list a.search-tag' )
        return {
            l.text: Danbooru( self ) + l.attrs[ 'href' ]
            for l in links
        }

danbooru = Danbooru( 'https://danbooru.donmai.us/' )
