#!/usr/bin/env python

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
 
class Sites(object):
    pass
#----------------------------------------------------------------------
def loadSession():
    engine = create_engine('postgresql://postgres@localhost/sead', isolation_level='READ COMMITTED')

    metadata = MetaData(engine)
    sites = Table('tbl_sites', metadata, autoload=True)
    mapper(Sites, sites)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

#if __name__ == "__main__":
#    session = loadSession()
#    res = session.query(Sites).all()
#    for r in res:
#        print r.site_name
