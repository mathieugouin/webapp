"""Main web app entry point using Flask for Google App Engine."""
import logging
import flask  # Flask, request, render_template

import mgouinlib as MGL

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

    arg = "icao-station-identifier-name1"
    args = flask.request.args
    # Long name to match previous FG URL (this will include .TXT, ex: CYHU.TXT)
    if args is not None and arg in args:
        station = args.get(arg).upper()
        if len(station) > 0:
            lines = MGL.fgHandler(station)
            response_text = "\n".join(lines)

            response = flask.Response(
                response=response_text,
                content_type="text/plain; charset=us-ascii"
            )
            return response

        return "no metar"
    return "no metar"




@app.route('/test')
def test_route():
    """Dummy test route for local testing of Flask features."""
    html = flask.render_template('test.html',
                           greeting='Hello you',
                           p_list=['a', 'b', 'hello you', '2 > 3', '     '])
    logging.debug(html)
    return html

    # name = request.args.get('name')
    # return f'Hello, {name}' if name else 'Hello, World!'


if __name__ == '__main__':
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
