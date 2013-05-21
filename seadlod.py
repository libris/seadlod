#!/usr/bin/env python

from flask import Flask, render_template

from database import Site, Biblio
import database

import urllib, urllib2
import xml.etree.ElementTree as etree

app = Flask(__name__)

@app.route("/")
def hello():
    return "At the root"

@app.route("/site/<int:site_id>")
def site(site_id):
    site = session.query(Site).filter(Site.site_id == site_id).first()
    return render_template("site.html", site = site, raaIdentifier = getRAAIdentifier(site.national_site_identifier))

@app.route("/biblio/<int:biblio_id>")
def biblio(biblio_id):
    biblio = session.query(Biblio).filter(Biblio.biblio_id == biblio_id).first()
    return render_template("biblio.html", biblio = biblio)


def getRAAIdentifier(itemNumber):
    identifier = None
    if itemNumber:
        if not ':' in itemNumber:
            itemNumber = itemNumber + ':1'
        itemNumber = "itemNumber=\"%s\"" % itemNumber
        #itemNumber = "=".join(["\"itemNumber", "\""+itemNumber+"\""])
        print "itemNumber", itemNumber, type(itemNumber)
        query = {
            u'x-api': u'test',
            u'method': u'search',
            u'recordSchema': u'xml',
            u'fields': u'itemId',
            u'query': itemNumber.encode('utf-8')
        }
        print "query", query
        print "queryString", urllib.urlencode(query)
        url = urllib2.urlopen(u'http://kulturarvsdata.se/ksamsok/api?%s' % urllib.urlencode(query))
        xml = etree.parse(url)
        root = xml.getroot()
        identifier = root.findall('.//field')[0]
        url.close()
        print "Identifier", identifier.text
    return identifier.text



if __name__ == "__main__":
    session = database.loadSession()

    from optparse import OptionParser
    oparser = OptionParser()
    oparser.add_option('-d', '--debug', action='store_true', default=False)
    opts, args = oparser.parse_args()
    app.debug = opts.debug
    app.run(host='0.0.0.0')
