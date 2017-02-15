from flask import Blueprint, request, jsonify
from flask_mail import Message

from bootstrap import mail
import config.main as conf
from lib.auth import hashfunc, validate_new_password
from models.user import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["POST"])
def email_registration():
    """
    Email registration.
    Requires email, password, and password_confirmation params.
    A verification email will be sent to the email address provided."""
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')
    callback_url = request.form.get('confirm_success_url')

    if not validate_new_password(password, password_confirmation):
        resp = {"status": "error",
                "errors": {"password_confirmation": ["doesn't match "
                                                     "Password"]}}
    else:
        resp = {"status": "success"}
        user = User(name=email, login=email, email=email,
                    password=hashfunc(password),
                    role="user")
        user.save()
        mail_body = conf.REGISTER_MAIL_BODY.format(callback_url=callback_url)
        msg = Message(conf.REGISTER_MAIL_SUBJECT,
                      sender=conf.FROM_ADDR,
                      reply_to=conf.FROM_ADDR,
                      recipients=[email])
        msg.body = """
    From: %s <%s>
    %s
    """ % (conf.FROM_NAME, conf.FROM_ADDR, mail_body)
        mail.send(msg)
    return resp


@auth_bp.route("/", methods=["DELETE"])
def delete_account():
    """
    Account deletion.
    This route will destroy users identified by their uid, access_token and
    client headers.
    """
    uid = request.headers.get("uid")
    access_token = request.headers.get("access-token")
    client = request.headers.get("client")
    error = False
    try:
        user = User.objects.get(_id=uid)
        if user.is_token_valid(access_token, client):
            user.delete()
        else:
            error = True
    except (User.DoesNotExist, KeyError):
        error = True
    if error:
        return jsonify({
          "status": "error",
          "errors": ["User was not found or was not logged in."]
        })
    else:
        return jsonify({"success": True,
                        "message": "Your account has been deleted."
                                   " See you soon maybe :)"})


@auth_bp.route("/", methods=["PUT"])
def update_account():
    """
    Account updates.
    This route will update an existing user's account settings.
    The default accepted params are password and password_confirmation,
    but this can be customized using the devise_parameter_sanitizer
    system. If config.check_current_password_before_update is set
    to :attributes the current_password param is checked before
    any update, if it is set to :password the current_password
    param is checked only if the request updates user password.
    """
    pass
    # TODO


@auth_bp.route("/sign_in", methods=["POST"])
def signin():
    """
    Email authentication.
    Requires email and password as params.
    This route will return a JSON representation of the User model
    on successful login along with the access-token and client in
    the header of the response."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = User.objects.get(email=email,
                                password=hashfunc(password))
        resp = jsonify(uid=user._id,
                       provider=user.provider,
                       email=user.email,
                       name=user.name,
                       role=user.role)
        token = user.generate_token()
        resp.headers.update(token)
        return resp
    except User.DoesNotExist:
        return jsonify({
              "status": "error",
              "errors": ["Invalid login credentials. Please try again."]
                })


@auth_bp.route("/sign_out", methods=["DELETE"])
def signout():
    """
    Use this route to end the user's current session.
    This route will invalidate the user's authentication token.
    You must pass in uid, client, and access-token in the request headers."""
    uid = request.headers.get("uid")
    access_token = request.headers.get("access-token")
    client = request.headers.get("client")
    try:
        user = User.objects.get(_id=uid)
        user.invalidate_token(access_token, client)
        return jsonify({"success": True})
    except (User.DoesNotExist, KeyError):
        return jsonify({
          "errors": ["User was not found or was not logged in."]
        })


@auth_bp.route("/<provider>", methods=["GET"])
def sso(provider):
    """
    Set this route as the destination for client authentication.
    Ideally this will happen in an external window or popup.
    """
    pass
    # TODO


@auth_bp.route("/<provider>/callback", methods=["GET", "POST"])
def sso_callback(provider):
    """
    Destination for the oauth2 provider's callback uri.
    postMessage events containing the authenticated user's data
    will be sent back to the main client window from this page.
    """
    pass
    # TODO


@auth_bp.route("/validate_token", methods=["GET"])
def validate_token():
    """
    Use this route to validate tokens on return visits to the client.
    Requires uid, client, and access-token as params.
    These values should correspond to fields in your User model.
    """
    uid = request.headers.get("uid")
    access_token = request.headers.get("access-token")
    client = request.headers.get("client")
    try:
        user = User.objects.get(_id=uid)
        user.invalidate_token(access_token, client)
        token = user.generate_token(client)
        resp = jsonify({"success": True,
                        "data": user.dump()})
        resp.headers.update(token)
        return resp
    except (User.DoesNotExist, KeyError):
        return jsonify({"success": False,
                        "errors": ["User not found or access-token invalid."]})


@auth_bp.route("/password", methods=["PUT"])
def password_edit():
    """
    Use this route to change users' passwords.
    Requires password and password_confirmation as params.
    This route is only valid for users that registered by email
        (OAuth2 users will receive an error).
    It also checks current_password if
    config.check_current_password_before_update is not set false
    (disabled by default).
    """
    uid = request.headers.get("uid")
    access_token = request.headers.get("access-token")
    client = request.headers.get("client")
    error = False
    errors = {}
    try:
        user = User.objects.get(_id=uid)
        if user.is_token_valid(access_token,
                               client) and user.provider == "email":
            password = request.form.get('password')
            password_confirmation = request.form.get('password_confirmation')
            if validate_new_password(password, password_confirmation):
                user.password = hashfunc(password)
                user.save()
        else:
            error = True
            errors["password_confirmation"] = ["doesn't match Password"],
    except (User.DoesNotExist, KeyError):
        error = True
        errors["full_message"] = ["Request is invalid"]
    if error:
        return jsonify({"success": False,
                        "errors": errors})
    else:
        return jsonify({"success": True,
                        "data": {
                            "message": "Your password has been "
                                       "successfully updated."
                        }})


@auth_bp.route("/password", methods=["POST"])
def password_reset():
    """
    Use this route to send a password reset confirmation email
    to users that registered by email.
    Accepts email and redirect_url as params.
    The user matching the email param will be sent instructions
    on how to reset their password.
    redirect_url is the url to which the user will be redirected after
    visiting the link contained in the email.
    """
    email = request.form.get('email')
    redirect_url = request.form.get('redirect_url')
    mail_body = conf.PWD_RESET_MAIL_BODY.format(callback_url=redirect_url)
    msg = Message(conf.REGISTER_MAIL_SUBJECT,
                  sender=conf.FROM_ADDR,
                  reply_to=conf.FROM_ADDR,
                  recipients=[email])
    msg.body = """
From: %s <%s>
%s
""" % (conf.FROM_NAME, conf.FROM_ADDR, mail_body)
    mail.send(msg)
    return {"success": True,
            "message": "An email has been sent containing instructions "
                       "for resetting your password."}


@auth_bp.route("/password/edit", methods=["GET"])
def password_reset_confirm():
    """
    Verify user by password reset token.
    This route is the destination URL for password reset confirmation.
    This route must contain reset_password_token and redirect_url params.
    These values will be set automatically by the confirmation email
    that is generated by the password reset request.
    """
    pass
    # TODO
