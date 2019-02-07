import webapp2
import mgouinlib as MGL

################################################################################
# Notes:
# NEW https://tgftp.nws.noaa.gov/data/observations/metar/stations/CYHU.TXT
# OLD http://tgftp.nws.noaa.gov/data/observations/metar/stations/CYHU.TXT
# MG  http://mgouin.appspot.com/fg?icao-station-identifier-name1=CYHU.TXT
# 
# http://localhost:8080/fg?icao-station-identifier-name1=CYHU.TXT
################################################################################

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/plain; charset=us-ascii"

        # Long name to match previous FG URL (this will include .TXT, ex: CYHU.TXT)
        station = self.request.get("icao-station-identifier-name1").upper()

        lines = MGL.fgHandler(station)

        for l in lines:
            self.response.write(l + "\n")

app = webapp2.WSGIApplication([(r'/.*', MainPage)], debug=True)

