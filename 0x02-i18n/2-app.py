#!/usr/bin/env python3
"""
Flask app with Babel for internationalization.
"""

from flask import Flask, render_template, request
from flask_babel import Babel

class Config:
    """
    Configuration class for Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """
    Select the best match for supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def home() -> str:
    """
    Render the homepage with a welcome message.
    """
    return render_template('2-index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
