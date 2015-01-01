import os
import itertools

import pytest

import blaze as bz
from kdbpy import kdb as k
from kdbpy.kdb import DEFAULT_PORT_RANGE, Credentials
from kdbpy.exampleutils import example_data

syms = itertools.count()


@pytest.fixture
def gensym():
    return 'sym%d' % next(syms)


@pytest.fixture(scope='session')
def creds():
    # must be session scoped because of downstream usage
    return Credentials(port=DEFAULT_PORT_RANGE[0])

@pytest.fixture(scope='session')
def creds2():
    # must be session scoped because of downstream usage
    return Credentials(port=DEFAULT_PORT_RANGE[0]+1)

@pytest.yield_fixture(scope='module')
def kq(creds):
    with k.KQ(creds,start=True) as kq:
        yield kq

@pytest.fixture(scope='module')
def kdb(kq):
    kq.read_kdb(os.path.join(os.path.dirname(__file__), 'conftest.q'))
    return kq


@pytest.fixture(scope='module')
def db(kdb):
    return bz.Data(kdb)


@pytest.fixture(scope='module')
def par(kdbpar):
    return bz.Data(kdbpar)


@pytest.fixture(scope='module')
def kdbpar(kq):
    path = example_data(os.path.join('start', 'db'))
    assert os.path.exists(path)
    kq.read_kdb(path)
    return kq


@pytest.fixture
def df(kdb):
    return kdb.eval('t')


@pytest.fixture
def date_df(kdb):
    return kdb.eval('date_t')


@pytest.fixture
def rdf(kdb):
    return kdb.eval('rt')


@pytest.fixture
def sdf(kdb):
    return kdb.eval('st')


@pytest.fixture(scope='session')
def rstring(creds):
    return 'kdb://%s@%s:%d' % (creds.username, creds.host, creds.port)
