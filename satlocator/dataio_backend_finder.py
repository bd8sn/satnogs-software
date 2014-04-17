# -*- coding: utf-8 -*-

DATAIO_BACKEND = 'SQLITE'  # TODO:should be retrieved parametrically from config

if 'SQLITE' == DATAIO_BACKEND:
    import dataio_sqlite as dataio_backend
#elif '' == DATAIO_BACKEND:
#    pass