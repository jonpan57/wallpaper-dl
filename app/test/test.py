import requests

session = requests.session()


def test(a, **options):
    b = options.get('file')
    print(a)
    print(b)


test('12', file='312')
