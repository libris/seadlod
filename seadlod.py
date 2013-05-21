#!/usr/bin/env python

from flask import Flask, render_template

from database import Sites
import database

app = Flask(__name__)

@app.route("/")
def hello():
    return "At the root"

@app.route("/site/<int:site_id>")
def site(site_id):
    site = session.query(Sites).filter(Sites.site_id == site_id).first()
    return render_template("site.html", site_name = site.site_name,
                           latitude = site.latitude_dd,
                           longitude = site.longitude_dd,
                           altitude = site.altitude
                          )

if __name__ == "__main__":
    session = database.loadSession()

    from optparse import OptionParser
    oparser = OptionParser()
    oparser.add_option('-d', '--debug', action='store_true', default=False)
    opts, args = oparser.parse_args()
    app.debug = opts.debug
    app.run(host='0.0.0.0')
