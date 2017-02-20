# FrontEnd

Frontend in front/

Need to have node, npm and yarn install in your system.

For Ubuntu:

    # sudo apt install nodejs npm
    # curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    # echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    # sudo apt update && sudo apt install yarn

To compile front, go into front/ and launch `yarn install`.
To begin to code with live update of your modifications launch `yarn start`.

# Backend

Backend part is in back/

To launch it, install freezed requirements (ideally in a venv):

    # pip install -r requirements.freeze.txt

And launch the gunicorn server:

    # gunicorn main:application

Note: This is not fit for production use. The gunicorn should receive requests via a proxy http server (apache2, nginx, ...) and some deamon management system should handle the gunicorn (systemd, supervisord, ...)
