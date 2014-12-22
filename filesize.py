
# This is a stripped version of the hurry.filesize module
# http://pypi.python.org/pypi/hurry.filesize/

alternative = [
    (1024 ** 5, ' PB'),
    (1024 ** 4, ' TB'), 
    (1024 ** 3, ' GB'), 
    (1024 ** 2, ' MB'), 
    (1024 ** 1, ' KB'),
    (1024 ** 0, (' byte', ' bytes')),
    ]

def size(bytes, system=alternative):
    for factor, suffix in system:
        if bytes >= factor:
            break
    amount = int(bytes/factor)
    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

