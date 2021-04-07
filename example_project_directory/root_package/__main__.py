from package_2.usecase import GetHelloQuery, GetHelloHandler

query = GetHelloQuery('depcheck')

handler = GetHelloHandler()

print(handler(query))
