from os.path import basename, dirname, join
from glob import glob

pwd = dirname(__file__)
for x in glob(join(pwd, '*.py')):
    if not basename(x).startswith('__'):
        mod = __import__(basename(x)[:-3], globals(), level=1)
