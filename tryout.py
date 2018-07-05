api_key = 'a1894416aafef699594319d11fc1a565db08'

client = Client(api_key=api_key)

parts = [str(d).split('-') for d in pandas.date_range('2015-04-01', '2018-07-01', freq='M')]
months = [part[0] + '/' + part[1] for part in parts]

per_page = 5000

for month in months:
    esr = client.esearch(db='pubmed', term='("{month}"[Date - Publication])'.format(month=month))
    print('Starting {month} with {count} total articles'.format(month=month, count=esr.count))
    for i in range(0, esr.count, per_page):
        filename = 'dump/pubmed-{month}-{start}-{end}.xml'.format(month=month.replace('/', '-'), start=i, end=i + per_page)
        with open(filename, 'wb') as f:
            for i in range(0, 4):
                try:
                    result = client.efetch({
                      'db': 'pubmed',
                      'WebEnv': esr.webenv,
                      'query_key': esr.querykey,
                      'retmax': per_page,
                      'retstart': i
                    })
                    f.write(result)
                    print(filename)
                    break
                except:
                    print("\n")
                    print("Failed " + i + "times")
                    time.sleep(pow(2, i + 3))
