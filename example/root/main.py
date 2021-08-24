from bar.usecase import GetHelloQuery, GetHelloHandler

query = GetHelloQuery('depcheck')

handler = GetHelloHandler()

print(handler(query))
