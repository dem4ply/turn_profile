from elasticsearch_dsl.connections import connections

connections.configure(
    default={
        'hosts': [ 'waifus:80' ],
        'timeout': 3000,
    },
)
