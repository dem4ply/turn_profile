#!/usr/bin/env python
import requests
import sys
from pprint import pprint as print
import time


host = sys.argv[1]


headers = {
    'Authorization': 'Token {}'.format( sys.argv[2] )
}


response = requests.get( "{}packages/".format( host ), headers=headers )
packages = response.json()
print( '-' * 10 )
print( 'all packages' )
print( '-' * 10 )
print( packages )


response = requests.get(
    "{}packages/{}/".format( host, packages[0][ 'pk' ], ), headers=headers )

package = response.json()
print( '-' * 10 )
print( 'package 1' )
print( '-' * 10 )
print( package )


response = requests.post(
    "{}packages/{}/check/".format( host, packages[0][ 'pk' ], ), headers=headers )


print( '-' * 10 )
print( 'check invalid' )
print( '-' * 10 )
print( response.json() )


response = requests.post(
    "{}packages/{}/check/".format( host, packages[0][ 'pk' ], ),
    json={
        'ssn': '123456789', 'last_name': 'joe', 'first_name': 'jonh',
        '_use_factory': 'default' },
    headers=headers )

profile_url = response.headers[ 'Location' ]

print( '-' * 10 )
print( 'profile 1' )
print( '-' * 10 )
response = requests.get( profile_url, headers=headers )
profile = response.json()
print( profile )

time.sleep( 10 )
print( '-' * 10 )
print( 'profile 2' )
print( '-' * 10 )
response = requests.get( profile_url, headers=headers )
profile = response.json()
print( profile )


pass
