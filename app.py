import json

from bokeh.embed import components, json_item
from bokeh.plotting import figure
from bokeh.resources import INLINE
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
