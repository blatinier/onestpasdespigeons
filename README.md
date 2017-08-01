Health master: [![Code Health](https://landscape.io/github/blatinier/onestpasdespigeons/master/landscape.svg?style=plastic)](https://landscape.io/github/blatinier/onestpasdespigeons/master)

Health devel: [![Code Health](https://landscape.io/github/blatinier/onestpasdespigeons/devel/landscape.svg?style=plastic)](https://landscape.io/github/blatinier/onestpasdespigeons/devel)

Travis master: [![Travis](https://travis-ci.org/blatinier/onestpasdespigeons.svg?branch=master)](https://travis-ci.org/blatinier/onestpasdespigeons.svg?branch=master)

Travis devel: [![Travis](https://travis-ci.org/blatinier/onestpasdespigeons.svg?branch=devel)](https://travis-ci.org/blatinier/onestpasdespigeons.svg?branch=devel)

Coverage master: [![Coverage Status](https://coveralls.io/repos/github/blatinier/onestpasdespigeons/badge.svg?branch=mastre)](https://coveralls.io/github/blatinier/onestpasdespigeons?branch=master)

Coverage devel: [![Coverage Status](https://coveralls.io/repos/github/blatinier/onestpasdespigeons/badge.svg?branch=mastre)](https://coveralls.io/github/blatinier/onestpasdespigeons?branch=devel)


# Backend

Backend part is in pigeon/

To launch it, install freezed requirements (ideally in a venv):

    # pip install -r requirements/freeze.pip

And launch the gunicorn server:

    # gunicorn pigeon.wsgi:application

Note: This is not fit for production use. The gunicorn should receive requests via a proxy http server (apache2, nginx, ...) and some deamon management system should handle the gunicorn (systemd, supervisord, ...)
