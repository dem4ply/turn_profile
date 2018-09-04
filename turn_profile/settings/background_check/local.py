from tetrapod.bgc import bgc, connections

connections.configure(
    default={
        'user': '',
        'password': '',
        'account': '',
        'host': 'https://direct2m.backgroundchecks.com/integration/bgcdirectpost.aspx',
    }
)
