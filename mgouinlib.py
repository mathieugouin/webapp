"""Principal library."""

import logging
import re
import html as htmllib  # TBD rename local vars html to something else.
import urllib.parse
import xml.etree.ElementTree as ET

import requests


################################################################################
# Notes:
# https://appengine.google.com/
# https://code.google.com/apis/console/
# https://developers.google.com/places/documentation/search
################################################################################

GOOGLE_API_KEY = "AIzaSyBzHSfl-SZJpgCwSTnAhHjlDH5W3BDIMDk"
BLANK_LINE = ""
GOOGLE_SENSOR = "false"

################################################################################
def myLog(message):
    logging.info("[DEV_DEBUG]: " + str(message))


################################################################################
def readUrlAll(url, params=None):
    html = ""
    try:
        response = requests.get(
            url,
            params=params,
            allow_redirects=True,
            timeout=1
        )
        html = response.text
    except:
        pass
    return html

################################################################################
def readUrl(url, params=None):
    return readUrlAll(url, params).splitlines()

################################################################################
def htmlEscape(line):
    return htmllib.escape(line)

################################################################################
def encodeDict(in_dict):
    out_dict = {}
    for k, v in in_dict.items():
        if not v.isascii():
            v = v.encode('utf8')
        # TBD...
        # elif isinstance(v, str):
        #     # Must be encoded in UTF-8
        #     v.decode('utf8')
        out_dict[k] = v
    return out_dict

################################################################################
def surroundDiv(line):
    return "<div>" + line + "</div>\n"

################################################################################
def processBlankLine(line):
    if line == BLANK_LINE:
        return "&nbsp;"
    return line

################################################################################
def processLine(line):
    if line == BLANK_LINE:
        return surroundDiv("&nbsp;")
    return surroundDiv(htmlEscape(line))

################################################################################
def findStation(txt, icao = False):
    lines = []
    if icao: # find exactly the ICAO code
        txt = r"^.{20}\b" + txt.strip() + r"\b"
    for l in readUrl("http://weather.rap.ucar.edu/surface/stations.txt"):
        if re.search(txt, l, re.IGNORECASE):
            lines.append(l)
    return lines

################################################################################
def _getMetar1(station):
    """This version is not as reliable as the v2."""
    station = station.upper()
    metarLines = []
    for l in readUrl("https://tgftp.nws.noaa.gov/data/observations/metar/stations/" + station + ".TXT"):
        if re.search('was not found on this server', l):
            break
        if re.search(station, l):
            metarLines.append(l)
    logging.info(metarLines)
    return metarLines

################################################################################
def _getMetar2(station):
    station = station.upper()
    metarLines = []
    url = "https://aviationweather.gov/cgi-bin/data/metar.php?ids=" + station + \
          "&hours=0&order=id%2C-obs&sep=true"
    html = readUrlAll(url)
    match = re.search(station, html, re.MULTILINE | re.DOTALL)
    if match:
        metarLines.append(html.strip())
    logging.info(metarLines)
    return metarLines

################################################################################
def getMetar(station):
    """Selector btw versions."""
    # return _getMetar1(station)
    return _getMetar2(station)

################################################################################
def getTaf(station):
    lines = []
    #      https://aviationweather.gov/cgi-bin/data/taf.php?ids=CYHU&sep=true
    url = "https://aviationweather.gov/cgi-bin/data/taf.php?ids=" + station + "&sep=true"
    html = readUrlAll(url)
    match = re.search(
        r'\b' + station + r'\b',
        html,
        re.MULTILINE | re.DOTALL
        )
    if match:
        for l in html.split('\n'):
            l = l.strip()
            if l != "":
                lines.append(l)
                lines.append(BLANK_LINE)
        if len(lines) >= 2:
            lines.pop() # remove last blank line
    return lines

################################################################################
def metarHandler(station):
    lines = []
    station = station.upper()
    if len(station) > 0:  # user provided a station
        metarLines = getMetar(station)
        if len(metarLines) > 0:  # metar data available
            stationName = findStation(station, icao=True)
            if len(stationName) > 0:
                match = re.match(r"^(...................)", stationName[0])
                if match:
                    lines.append(match.group(1).strip())
            lines += metarLines
            # Find taf data
            tafLines = getTaf(station)
            if len(tafLines) > 0:
                lines.append(BLANK_LINE)
                lines += tafLines
        else: # metar data not found
            for l in findStation(station, icao=False):  # try to find the name of the station
                #                    CO GRAND JUNCTION   KGJT  GJT
                match = re.match(r"^(.............................)", l)
                if match:
                    lines.append(match.group(1))
                    lines.append(BLANK_LINE)
            if len(lines) >= 2:
                lines.pop() # remove last blank line
    else:
        lines = ["METAR & TAF Syntax: @metar <station>",
                 "Example: @metar KJFK",
                 BLANK_LINE,
                 "Airport Finder Syntax: @metar <keyword>",
                 "Example: @metar miami"]

    return lines

################################################################################
# FlightGear metar proxy handler
def fgHandler(station):
    lines = []
    station = station.upper()
    logging.debug("fgHandler %s", station)
    if len(station) > 0: # user provided a station
        url = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/" + station
        metarLines = readUrl(url)
        if len(metarLines) > 0: # metar data available
            lines += metarLines
    return lines

################################################################################
def gmlsGetInfo(ref):
    params = {'reference' : ref,
              'sensor' : GOOGLE_SENSOR,
              'key' : GOOGLE_API_KEY}
    url = "https://maps.googleapis.com/maps/api/place/details/xml?"
    url += urllib.urlencode(encodeDict(params))
    lines = []
    try:
        f = urllib.urlopen(url)
        root = ET.parse(f).getroot()
        if root.find('status').text == 'OK':
            for result in root.findall('result'):
                for key in ['name', 'formatted_address', 'formatted_phone_number']:
                    element = result.find(key)
                    if element is not None:
                        value = element.text
                        if value is not None:
                            lines.append(value)

    except:
        pass

    return lines

################################################################################
def gmlsHandler(query):
    lines = []
    params = {'query' : query,
              'sensor' : GOOGLE_SENSOR,
              'key' : GOOGLE_API_KEY}
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?"
    url += urllib.urlencode(encodeDict(params))
    try:
        f = urllib.urlopen(url)
        root = ET.parse(f).getroot()
        if root.find('status').text == 'OK':
            results = root.findall('result')
            for i in range(min(10, len(results))):
                result = results[i]
                ref = result.find("reference").text
                infoLines = gmlsGetInfo(ref)
                s = "#%d. " % (i + 1)
                if len(infoLines) > 0:
                    s += infoLines.pop(0) # put place title with the number
                lines.append(s)
                lines += infoLines
                lines.append(BLANK_LINE)
            if len(lines) >= 2:
                lines.pop() # remove last blank line
    except:
        pass

    return lines

################################################################################
def outputTest(lines):
    for l in lines:
        print(processLine(l)),

################################################################################
def gmlsTest():
    #query = u"caf\xe9 \xe0 montr\xe9al"
    query = "Hotel Humnabad"
    # None
    #ref = 'CoQBcgAAAJmSjg3Uwbx33GmWZQiOPr6dgz0z3oTEAbNDJR-5vcplOE_yM3Op2fsJNX5Idtja4QC5FAZgDltjN8jeVd1voMdZkY-o0KlTVatR9XgIqmWN19F0znuCewl0rgTc98Z5gwBZcqCTA7D43p2B5mGRp0wA9nETYm3p4yoftYWCAH-0EhDcQfduXY39jVnd_RsU6AkaGhQgDJ3nGr7cr9-fapWSwjrDIBkeZQ'
    # Exception
    ref = 'CnRqAAAA92F_r2BsbckojgZRSf-ddUNServOYtrsygt-LMHlZaO_akMRaqz50Oi6ihi6dRPp7vjv1e8QzIKN67u6igRff9qbQfSl3g45zUaYH8aazVN7iwxhSNXvAd7HLa6Wea22TnP5UfmNKVQgpOFx73cnBxIQTzU8pjOV1hd_80u1UKD_RxoU8dl6Af6a-kwDhPZxa7dZFugks6E'
    print(query)
    print(urllib.parse.quote(encodeDict({'q' : query})))
    outputTest(gmlsHandler(query))
    outputTest(gmlsGetInfo(ref))

################################################################################
def metarTest():
    station = "CYHU"
    #print _getMetar1(station) == _getMetar2(station)
    #print _getMetar1(station)
    #print _getMetar2(station)
    #outputTest(getTaf(station))
    outputTest(metarHandler(station))
    #outputTest(findStation(station, True))

################################################################################
def fgHandlerTest():
    stations = ["CYHU", "KLAX"]
    for station in stations:
        logging.info(fgHandler(station + ".TXT"))

################################################################################
def urlTest():
    # app log from txt web request
    s = "txtweb-message=caf%C3%A9%20%C3%A0%20montreal"
    print(dict(urllib.parse.parse_qsl(s)))

################################################################################
def _main():
    myLog("myLog(): Hello")
    fgHandlerTest()
    metarTest()
    # gmlsTest()
    urlTest()

if __name__ == '__main__':
    logging.basicConfig(
        # level=logging.DEBUG,
        level=logging.INFO,
        format='%(asctime)s%(msecs)03d %(name)-6s %(levelname)-8s %(filename)s:%(lineno)d %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S.',
        force=True
        )

    _main()
