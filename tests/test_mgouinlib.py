import logging
import mgouinlib as mgl


def test_output():
    lines = ['hello', 'bye']
    for l in lines:
        print(mgl.processLine(l))


def test_gmls():
    #query = u"caf\xe9 \xe0 montr\xe9al"
    query = "Hotel Humnabad"
    # None
    #ref = 'CoQBcgAAAJmSjg3Uwbx33GmWZQiOPr6dgz0z3oTEAbNDJR-5vcplOE_yM3Op2fsJNX5Idtja4QC5FAZgDltjN8jeVd1voMdZkY-o0KlTVatR9XgIqmWN19F0znuCewl0rgTc98Z5gwBZcqCTA7D43p2B5mGRp0wA9nETYm3p4yoftYWCAH-0EhDcQfduXY39jVnd_RsU6AkaGhQgDJ3nGr7cr9-fapWSwjrDIBkeZQ'
    # Exception
    ref = 'CnRqAAAA92F_r2BsbckojgZRSf-ddUNServOYtrsygt-LMHlZaO_akMRaqz50Oi6ihi6dRPp7vjv1e8QzIKN67u6igRff9qbQfSl3g45zUaYH8aazVN7iwxhSNXvAd7HLa6Wea22TnP5UfmNKVQgpOFx73cnBxIQTzU8pjOV1hd_80u1UKD_RxoU8dl6Af6a-kwDhPZxa7dZFugks6E'
    logging.info(query)
    # print(urllib.parse.quote(encodeDict({'q' : query})))
    # TBD
    # mgl.outputTest(mgl.gmlsHandler(query))
    # mgl.outputTest(mgl.gmlsGetInfo(ref))

def test_metar():
    station = "CYHU"
    #print getMetar(station) == getMetar2(station)
    #print getMetar(station)
    #print getMetar2(station)
    #outputTest(getTaf(station))
    mgl.outputTest(mgl.metarHandler(station))
    #outputTest(findStation(station, True))

def test_fgHandler():
    stations = ["CYHU", "KLAX"]
    for station in stations:
        logging.info(mgl.fgHandler(station + ".TXT"))

# TBD
# def test_url():
#     # app log from txt web request
#     s = "txtweb-message=caf%C3%A9%20%C3%A0%20montreal"
#     print(dict(urllib.parse.parse_qsl(s)))


def test_log():
    mgl.myLog("myLog(): Hello")

