#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

import conf
from bootstrap import application


@application.route("/", methods=['GET'])
def home():
    return render_template('index.html')
