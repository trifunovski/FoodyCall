from flask import Flask
from flask import render_template
from lib.menu.menu import menu
from lib.ratings.ratings import ratings
from lib.order.order import order
from lib.smshook.smshook import smshook
app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(ratings, url_prefix='/ratings')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(smshook,url_prefix='/smshook')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
