#! /usr/bin/env python
# -*- coding: utf-8 -*-
import config.main as conf
from bootstrap import application
from api.auth import auth_bp


application.register_blueprint(auth_bp)
