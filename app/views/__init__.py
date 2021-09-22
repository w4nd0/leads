from flask import Flask

from .lead_view import bp as bp_lead

def init_app(app: Flask):
    app.register_blueprint(bp_lead)