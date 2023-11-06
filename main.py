import logging
from flask import Flask, request, render_template


logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format='%(asctime)s%(msecs)03d %(name)-6s %(levelname)-8s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S.',
    force=True
    )


app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    # TBD not working...
    # html = render_template('templates/greeting.html', greeting='Hello you')
    # logging.debug(html)

    name = request.args.get('name')
    return f'Hello, {name}' if name else 'Hello, World!'


if __name__ == '__main__':
    app.run(port=8080)
