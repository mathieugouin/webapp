from flask import Flask

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
