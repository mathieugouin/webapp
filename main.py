"""Main web app entry point using Flask for Google App Engine."""
import logging
import flask  # Flask, request, render_template

import mgouinlib as mgl
# import sendmail

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format='%(asctime)s%(msecs)03d %(name)-6s %(levelname)-8s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S.',
    force=True
    )


# Create the Flask app
app = flask.Flask(
    __name__,
    # static_url_path='/static',
    # template_folder='/templates',
    )


# - url: /gmls
# - url: /metar         DONE
# - url: /fg            DONE
# - url: /mailer        TBD
# - url: /.*            DONE


@app.route('/')
def home_route():
    """Route of the root url."""
    return flask.render_template('index.html')


################################################################################
# Notes:
# NEW https://tgftp.nws.noaa.gov/data/observations/metar/stations/CYHU.TXT
# OLD http://tgftp.nws.noaa.gov/data/observations/metar/stations/CYHU.TXT
# MG  http://mgouin.appspot.com/fg?icao-station-identifier-name1=CYHU.TXT
#
# http://localhost:8080/fg?icao-station-identifier-name1=CYHU.TXT
################################################################################
@app.route('/fg')
def fg_route():
    """Route for FlightGear (FG) metar proxy."""
    # Long name to match previous FG URL (this will include .TXT, ex: CYHU.TXT)
    arg = "icao-station-identifier-name1"
    args = flask.request.args
    if args is not None and arg in args:
        station = args.get(arg).upper()
        if len(station) > 0:
            lines = mgl.fgHandler(station)
            response_text = "\n".join(lines)

            response = flask.Response(
                response=response_text,
                content_type="text/plain; charset=us-ascii"
            )
            return response
        return "no metar"
    return "no metar"


@app.route('/mailer')
def mailer_route():
    """Route of the mailer url."""
    return "TBD not implemented"


@app.route('/metar')
def metar_route():
    """Route of the metar url."""
    html = ""
    station = ""
    # http://mgouin.appspot.com/metar?txtweb-message=CYHU
    arg = "txtweb-message"
    args = flask.request.args
    if args is not None and arg in args:
        station = args.get(arg).upper()

    lines = [mgl.processBlankLine(l) for l in mgl.metarHandler(station)]
    html = flask.render_template('metar.html', lines=lines)

    logging.info(html)
    return html


@app.route('/test')
def test_route():
    """Dummy test route for local testing of Flask features."""
    html = flask.render_template('test.html',
                           greeting='Hello you',
                           p_list=['a', 'b', 'hello you', '2 > 3', '     '])
    logging.info(html)
    return html

    # name = request.args.get('name')
    # return f'Hello, {name}' if name else 'Hello, World!'


if __name__ == '__main__':
    # sendmail.sendMailTest()

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(
        # host="127.0.0.1"
        port=8080,
        debug=True,
    )
