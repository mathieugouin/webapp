"""Main web app entry point using Flask for Google App Engine."""
import logging
from flask import Flask, request, render_template


logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format='%(asctime)s%(msecs)03d %(name)-6s %(levelname)-8s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S.',
    force=True
    )


# Create the Flask app
app = Flask(
    __name__,
    # static_url_path='/static',
    # template_folder='/templates',
    )


@app.route('/')
def home_route():
    """Route of the root url."""
    return render_template('index.html')


@app.route('/fg')
def fg_route():
    """Route for FlightGear (FG) metar proxy."""
    return ""
    #return render_template('index.html')


@app.route('/test')
def test_route():
    """Dummy test route for local testing of Flask features."""
    html = render_template('test.html',
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
