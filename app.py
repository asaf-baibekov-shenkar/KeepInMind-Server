import mysql.connector
from flask import Flask, request, jsonify, make_response
# import google.auth
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="KeepInMind"
)
cursor = db.cursor()

app = Flask(__name__)

#socres:
@app.route("/scores", methods=["POST"])
def add_score():
    try:
        data = request.get_json()
        username = data["username"]
        score = data["score"]

        sql = "INSERT INTO scores (username, score) VALUES (%s, %s)"
        val = (username, score)
        cursor.execute(sql, val)
        db.commit()

        return "Score added successfully"
        
    except KeyError:
        return make_response("Error: request data is missing required keys (username, score)", 400)

    except mysql.connector.Error as e:
        return make_response("Error: {}".format(e), 500)

@app.route("/scores", methods=["GET"])
def get_scores():
    try:
        cursor.execute("SELECT * FROM scores")
        scores = cursor.fetchall()

        return jsonify(scores)
    except mysql.connector.Error as e:
        return make_response("Error: {}".format(e), 500)

@app.route("/scores/<int:account_id>", methods=["GET"])
def get_score(account_id):
    try:
        cursor.execute("SELECT score FROM scores WHERE account_id = %s", (account_id,))
        score = cursor.fetchone()
        if not score:
            return make_response("Error: Score not found", 404)
        return jsonify(score)
    except mysql.connector.Error as e:
        return make_response("Error: {}".format(e), 500)


#accounts:
@app.route("/accounts", methods=["POST"])
def add_account():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        sql = "INSERT INTO accounts (username, password) VALUES (%s, %s)"
        val = (username, password)
        cursor.execute(sql, val)
        db.commit()

        return "Account added successfully"
    except KeyError:
        return make_response("Error: request data is missing required keys (username, password)", 400)
    except mysql.connector.Error as e:
        return make_response("Error: {}".format(e), 500)

@app.route("/accounts", methods=["GET"])
def get_accounts():
    try:
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        return jsonify(accounts)
    except mysql.connector.Error as e:
        return make_response("Error: {}".format(e), 500)

@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    try:
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
        account = cursor.fetchone()
        if not account:
            return make_response("Error: Account not found", 404)
        return jsonify(account)
    except mysql.connector.Error as e:
        return make_response("Error: {}".format(e), 500)

'''
#google photos tests:
@app.route("/photos", methods=["POST"])
def add_photo():
    try:
        data = request.get_json()
        photo_url = data["photo_url"]
    except KeyError:
        return make_response("Error: request data is missing required key (photo_url)", 400)

#google photos:
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

# oauth authorization flow to get an access token:
credentials = google.oauth2.credentials.Credentials.from_client_secrets_file(
    CLIENT_ID_FILE, scopes=["https://www.googleapis.com/auth/photoslibrary"]
)

service = build("photoslibrary", "v1", credentials=credentials)

def set_media_item(file_path, mime_type):
    new_media_item = {
        "newMediaItems": [{
            "description": "A beautiful photo",
            "simpleMediaItem": {
                "fileName": file_path
            }
        }]
    }
    try:
        service.mediaItems().batchCreate(newMediaItems=new_media_item).execute()
        print("Media item added to library.")
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_media_items():
    try:
        response = service.mediaItems().search(pageSize=25).execute()
        items = response.get("mediaItems", [])

        print(f"Found {len(items)} items:")

        for item in items:
            print(f"{item['filename']} ({item['mimeType']})")
            
        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            next_page_token = None

        while next_page_token is not None:
            response = service.mediaItems().search(
                pageSize=25, pageToken=next_page_token).execute()
            items = response.get("mediaItems", [])

            print(f"Found {len(items)} items:")

            for item in items:
                print(f"{item['filename']} ({item['mimeType']})")
            next_page_token = response.get("nextPageToken")

    except HttpError as error:
        print(f"An error occurred: {error}")
'''
