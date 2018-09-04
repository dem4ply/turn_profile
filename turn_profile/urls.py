from django.contrib import admin
from django.urls import path, include
from turn_users.urls import urlpatterns as turn_url_urls
from background_check.urls import urlpatterns as background_check_url_urls
from partners.urls import urlpatterns as partners_urls

urlpatterns = [
    #path( 'admin/', admin.site.urls ),
    path( r'', include( ( turn_url_urls, 'turn_users' ), namespace='users' ), ),
    path( r'', include(
        ( background_check_url_urls, 'background_checks' ),
        namespace='background_checks' ), ),
    path( r'', include(
        ( partners_urls, 'partners' ), namespace='partners' ), ),
]


def show_urls(urllist, depth=0):
    for entry in urllist:
        if ( hasattr( entry, 'namespace' ) ):
            print( "\t" * depth, entry.pattern.regex.pattern,
                   "[%s]" % entry.namespace )
        else:
            print( "\t" * depth, entry.pattern.regex.pattern,
                   "[%s]" % entry.name )
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)


show_urls( urlpatterns )
