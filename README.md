=== FrontEnd ===

Frontend in front/

To compile front, go into front/ and launch `yarn install`.
To begin to code with live update of your modifications launch `yarn start`.

=== Backend ===

Backend part is in back/

To launch it, install freezed requirements (ideally in a venv):

    # pip install -r requirements.freeze.txt

And launch the gunicorn server:

   # gunicorn main:application

Note: This is not fit fora production use. The gunicorn should receive requests via a proxy http server (apache2, nginx, ...) and some deamon management system should handle the gunicorn (systemd, supervisord, ...)
