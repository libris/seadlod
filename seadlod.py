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
    if not itemNumber.contains(':'):
        itemNumber = itemNumber + ':1'
    query = 'itemNumber="%s"' % urllib.urlencode(itemNumber)
    url = urllib2.urlopen('http://kulturarvsdata.se/ksamsok/api?x-api=test&method=search&query=%s&recordSchema=xml&fields=itemId' % query)
    xml = url.read()
    url.close()
    doc = etree.fromstring(xml)
    identifier = doc.xpath('/result/records[0]/record/field/@itemId')
    print "Identifier", identifier
    return identifier



if __name__ == "__main__":
    session = database.loadSession()

    from optparse import OptionParser
    oparser = OptionParser()
    oparser.add_option('-d', '--debug', action='store_true', default=False)
    opts, args = oparser.parse_args()
    app.debug = opts.debug
    app.run(host='0.0.0.0')
