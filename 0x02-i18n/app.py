#!/usr/bin/env python3
"""
Flask app with Babel for internationalization and user mock login.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

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

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user() -> dict:
    """
    Get user information based on the login_as URL parameter.
    """
    user_id = request.args.get('login_as')
    if user_id:
        try:
            user_id = int(user_id)
            return users.get(user_id)
        except ValueError:
            return None
    return None

@app.before_request
def before_request() -> None:
    """
    Execute before each request to set the global user.
    """
    g.user = get_user()

@babel.localeselector
def get_locale():
    """
    Select the best match for supported languages based on URL parameters,
    user settings, request headers, or default locale.
    """
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    
    # 2. Locale from user settings
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
    # 3. Locale from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """
    Select the best match for timezone based on URL parameters,
    user settings, or default to UTC.
    """
    # 1. Timezone from URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass
    
    # 2. Timezone from user settings
    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass
    
    # 3. Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def home() -> str:
    """
    Render the homepage with a welcome message and the current time.
    """
    if g.user:
        message = _('logged_in_as', username=g.user['name'])
    else:
        message = _('not_logged_in')
    
    # Get current time in the inferred timezone
    timezone = get_timezone()
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz).strftime('%b %d, %Y, %I:%M:%S %p') if tz else datetime.utcnow().strftime('%b %d, %Y, %I:%M:%S %p')
    
    return render_template('7-index.html', message=message, current_time=_('current_time_is', current_time=current_time))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
