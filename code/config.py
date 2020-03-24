import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2f9ed4a8-8dc6-418b-be81-583f35e8a222'
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or '1c68a939-55ca-4190-b40e-a59a0d5fe910'
    PUBLIC = os.environ.get('PUBLIC') or "static/public"
    MEDIA = os.environ.get('MEDIA') or "media/"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LDAP_PROTOCOL_VERSION = 3