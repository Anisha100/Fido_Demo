from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity
from fido2.server import Fido2Server
from flask import *
from storageoperations import *
import os
import pickle
import fido2.features
def read_key(name):
    try:
         
          x=pickle.loads(downloadpick(name))
         
          return x
    except:
          return []
         
def save_key(name, credentials):
     try:
         
          uploadpick(pickle.dumps(credentials), name)
          
          
     except:
          pass 
fido2.features.webauthn_json_mapping.enabled = True


app = Flask(__name__, static_url_path="")
if read_key("secret")==[]:
    save_key("secret",os.urandom(32))
app.secret_key =read_key("secret")   # Used for session.

rp = PublicKeyCredentialRpEntity(name="Demo server", id="localhost")
server = Fido2Server(rp)
credentials = []

@app.route("/api/register/begin", methods=["POST", "GET"])
def register_begin():
    username=request.args['username']
    credentials=read_key(username)
    options, state = server.register_begin(
        PublicKeyCredentialUserEntity(
            id=b"user_id",
            name="a_user",
            display_name="A. User",
        ),
        credentials,
        user_verification="discouraged",
        authenticator_attachment="platform",
    )

    session["state"] = state
    print("\n\n\n\n")
    print(options)
    print("\n\n\n\n")

    return jsonify(dict(options))


@app.route("/api/register/complete", methods=["POST","GET"])
def register_complete():
    username=request.args['username']
    credentials=read_key(username)
    response = request.json
    print("RegistrationResponse:", response)
    auth_data = server.register_complete(session["state"], response)

    credentials.append(auth_data.credential_data)
    print("REGISTERED CREDENTIAL:", auth_data.credential_data)
    save_key(username,credentials)
    return jsonify({"status": "OK"})
    


@app.route("/api/authenticate/begin", methods=["POST","GET"])
def authenticate_begin():
    username=request.args['username']
    credentials=read_key(username)

    if not credentials:
        abort(404)

    options, state = server.authenticate_begin(credentials)
    session["state"] = state

    return jsonify(dict(options))


@app.route("/api/authenticate/complete", methods=["POST", "GET"])
def authenticate_complete():
    username=request.args['username']
    credentials=read_key(username)
    if not credentials:
        abort(404)

    response = request.json
    print("AuthenticationResponse:", response)
    server.authenticate_complete(
        session.pop("state"),
        credentials,
        response,
    )
    print("ASSERTION OK")
    return jsonify({"status": "OK"})
@app.route("/")
def star():
    ip=request.remote_addr
    return render_template("index.html",ip=ip)
    
@app.route("/reg",methods=["GET"])
def register():
    username=request.args['username']
    return render_template("register.html",Anisha=username)
@app.route("/auth",methods=["GET"])
def authenticate():
     username=request.args['username']
     return render_template("authenticate.html",Anisha=username)
def main():  
    app.run(ssl_context="adhoc",host="0.0.0.0",port=5000, debug=False)


if __name__ == "__main__":
    main()
