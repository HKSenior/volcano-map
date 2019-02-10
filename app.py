from flask import Flask, render_template

from volcano.Map import Map


app = Flask(__name__)
map = Map('http://volcano.oregonstate.edu/volcano_table')
map.createMap()


@app.route('/')
def map():
    return render_template('volcano.html')


if __name__ == "__main__":
    app.run()