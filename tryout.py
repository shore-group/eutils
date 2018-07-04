from eutils import Client

api_key = 'a1894416aafef699594319d11fc1a565db08'

client = Client(api_key=api_key)

esr = client.esearch(db='pubmed', term='("2013/01/01"[Date - Publication] : "3000"[Date - Publication])')

per_page = 5000

for i in range(0, esr.count, per_page):
    with open('dump/pubmed-{start}-{end}.xml'.format(start=i, end=i + per_page), 'wb') as f:
        result = client.efetch({
          'db': 'pubmed',
          'WebEnv': esr.webenv,
          'query_key': esr.querykey,
          'retmax': per_page,
          'retstart': i
        })

        f.write(result)

