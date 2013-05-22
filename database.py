#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker, relationship, column_property
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres@localhost/sead', isolation_level='READ COMMITTED')
Base = declarative_base()

tbl_site_references = Table('tbl_site_references', Base.metadata,
     Column('site_id', Integer, ForeignKey('tbl_sites.site_id')),
     Column('biblio_id', Integer, ForeignKey('tbl_biblio.biblio_id'))
 )

tbl_sample_group_references = Table('tbl_sample_group_references', Base.metadata,
     Column('sample_group_id', Integer, ForeignKey('tbl_sample_groups.sample_group_id')),
     Column('biblio_id', Integer, ForeignKey('tbl_biblio.biblio_id'))
 )

class SampleGroup(Base):
    __tablename__ = 'tbl_sample_groups'
    __table_args__ = { 'autoload':True, 'autoload_with':engine }

class Publisher(Base):
    __tablename__ = 'tbl_publishers'
    __table_args__ = { 'autoload':True, 'autoload_with':engine }

class Biblio(Base):
    __tablename__ = 'tbl_biblio'
    __table_args__ = { 'autoload':True, 'autoload_with':engine, 'extend_existing': True }
    publisher_id = Column(Integer)

    sample_groups = relationship('SampleGroup', secondary=tbl_sample_group_references, backref='biblios')

    publisher_name = column_property(select([Publisher.publisher_name]).where(Publisher.publisher_id==publisher_id))
    place_of_publishing_house = column_property(select([Publisher.place_of_publishing_house]).where(Publisher.publisher_id==publisher_id))

class Site(Base):
    __tablename__ = 'tbl_sites'
    __table_args__ = { 'autoload':True, 'autoload_with':engine }

    biblios = relationship('Biblio', secondary=tbl_site_references, backref='sites')
    sample_groups = relationship('SampleGroup', foreign_keys=[SampleGroup.site_id], backref='site')

def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
