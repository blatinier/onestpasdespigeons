Health master: [![Code Health](https://landscape.io/github/blatinier/onestpasdespigeons/master/landscape.svg?style=plastic)](https://landscape.io/github/blatinier/onestpasdespigeons/master)
Health devel: [![Code Health](https://landscape.io/github/blatinier/onestpasdespigeons/devel/landscape.svg?style=plastic)](https://landscape.io/github/blatinier/onestpasdespigeons/devel)


# FrontEnd

Frontend in front/

To compile front, go into front/ and launch `yarn install`.
To begin to code with live update of your modifications launch `yarn start`.

# Backend

Backend part is in back/

To launch it, install freezed requirements (ideally in a venv):

    # pip install -r requirements.freeze.txt

And launch the gunicorn server:

    # gunicorn main:application

Note: This is not fit for production use. The gunicorn should receive requests via a proxy http server (apache2, nginx, ...) and some deamon management system should handle the gunicorn (systemd, supervisord, ...)
