from getpass import getuser


def postgres_url(
    dbname,
    driver='psycopg2',
    user=None,
    password=None,
    host='localhost',
    port=None,
    fallback_hosts=None,
    **kwargs,
):
    url = f'postgresql+{driver}://{user or getuser()}'

    if password is not None:
        url += f':{password}'

    url += f'@{host}'

    if port is not None:
        url += f':{port}'

    url += f'/{dbname}'
    options = [f'host={host}' for host in fallback_hosts or []]
    options.extend(f'{key}={value}' for key, value in kwargs.items())

    if len(options) > 0:
        url += '?' + '&'.join(options)

    return url


def sqlite_url(dbfile=None):
    url = 'sqlite://'

    if dbfile is not None:
        url += f'/{dbfile}'

    return url
