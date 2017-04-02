#! /usr/bin/env python
# -*- coding: utf-8 -*-
import config.main as conf
from urllib.parse import urlsplit
from flask import Flask
from flask_mail import Mail
import mongoengine

application = Flask(__name__)
application.config.from_object(conf)
application.debug = True
scheme, domain, _, _, _ = urlsplit(conf.PLATFORM_URL)
application.config['PREFERRED_URL_SCHEME'] = scheme

mail = Mail()
application.config["MAIL_SERVER"] = "smtp.gmail.com"
application.config["MAIL_PORT"] = 465
application.config["MAIL_USE_SSL"] = True
application.config["MAIL_USERNAME"] = conf.MAIL_SENDER_ADDR
application.config["MAIL_PASSWORD"] = conf.MAIL_SENDER_MDP

mail.init_app(application)

# Init mongoengine connection
mongoengine.connect(db=conf.MONGODB['db'],
                    host=conf.MONGODB['host'],
                    username=conf.MONGODB['user'],
                    password=conf.MONGODB['pwd'])