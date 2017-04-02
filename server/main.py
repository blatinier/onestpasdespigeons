#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

import config.main as conf
from bootstrap import application
from api.auth import auth_bp


def register_bps(app):
    app.register_blueprint(auth_bp)


register_bps(application)

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=5001, debug=False)
