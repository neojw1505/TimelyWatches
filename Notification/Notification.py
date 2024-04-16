from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flasgger import Swagger
from flask_cors import CORS
from sqlalchemy import func
from copy import deepcopy

'''
API Endpoints:
1. GET /notification/<string:email> - Get all notification that belongs to a user (email)
2. POST /notification/createNotification - create notification in the database  


PORT: 5004
DATABASE: Notification
TABLE: notification
SQL Credentials: root:root
SQL Port: 3306


SQL Database creation code:
CREATE TABLE Notification(
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT NOT NULL,
    auction_id INT,
    notification_type VARCHAR(50) NOT NULL COMMENT '(outbid, winandpayremind, paysucess,rollbackandpayremind, schedulesuccess)',
    time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_unread INT DEFAULT 1
);

'''
########## initiate flask ##########
app = Flask(__name__)  # initialize a flask application

# path = "Notification"
# set_database_uri(app, path)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:password@localhost:3306/Notification"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)
########## initiate swagger ##########
# Initialize flasgger
app.config['SWAGGER'] = {
    'title': 'Notification microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create and retrieve of notification. Additionally, it sends email to the user.'
}
swagger = Swagger(app)

########## database ##########
class Notification(db.Model):
    __tablename__ = 'Notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_id = db.Column(db.Integer, nullable=False)
    auction_id = db.Column(db.Integer)
    notification_type = db.Column(db.String(255), nullable=False)
    time_sent = db.Column(db.TIMESTAMP, server_default=func.timezone('Asia/Singapore', func.current_timestamp()))
    is_unread = db.Column(db.Integer, default=1)

    def __init__(self, recipient_id,notification_type, auction_id=None,is_unread=1):
        self.recipient_id = recipient_id
        self.notification_type = notification_type
        self.auction_id = auction_id
        self.is_unread = is_unread
        

    def json(self):
        return {
            "id": self.id,
            "recipient_id": self.recipient_id,
            "auction_id": self.auction_id,
            "notification_type": self.notification_type,
            "time_sent": self.time_sent.strftime('%Y-%m-%d %H:%M:%S'),
            "is_unread": self.is_unread,
        }


# 1. GET /notification/<int:user_id> - Get all notification that belongs to a user (id)
@app.route('/notification/<int:user_id>')
def find_notification_by_email(user_id):
    """
    Get all notification by user email
    ---
    parameters:
        -   name: user_id
            in: path
            type: integer
            required: true
            description: The user's id
    responses:
        200:
            description: retrieve all the notification that user has using the email passed in
        404:
            description: There is no such notification for this user.

    """

    
    #get all the notification that below to the specify user from the database
    allNotification = db.session.scalars(
        db.select(Notification).filter_by(recipient_id=user_id)).all()
    
    allNotification_copy = deepcopy(allNotification)

    #change is_unread notification to 0 after (they have read the notification)
    for eachNotif in allNotification:
        eachNotif.is_unread = 0

    db.session.commit()

    # print(allNotification)
    if len(allNotification):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "notifications": [notif.json() for notif in allNotification_copy]
                },
                "message": "retrieved notification successfully.",
                "error": "NA"
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {},
            "message": "There is no notification for this user",
            "error": "no notification for this user"
        }
    ), 404


# 2. POST /notification/createNotification - create notification in the database
@app.route('/notification/createNotification', methods=['POST'])
def create_notification():
    """
    Create a notification into the database
    ---
    requestBody:
        description: notification creation detail
        required: true
        content:
            application/json:
                schema:
                    properties:
                        recipient_id: 
                            type: integer
                            description: recipient_id
                        auction_id: 
                            type: integer
                            description: auction_id
                        notification_type: 
                            type: string
                            description: notification_type

    responses:
        201:
            description: notification created for user
        500:
            description: Internal server error. An error occurred add new notification to database

    """

    new_notif = request.get_json()

    
    #initialise new notification
    new_notification = Notification(recipient_id=new_notif["recipient_id"], notification_type=new_notif["notification_type"], auction_id=new_notif["auction_id"])
    try:
        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        print(f"Notification microservice: fail to add new notification") 
        return jsonify({
            "code":500,
            "data":{},
            "message": "An error occurred add new notification to database.",
            "error": str(e),
        }),500
    
    return jsonify({
        "code":201,
        "data":new_notif,
        "message": "added notification into the database successfully.",
        "error": "NA",
    }),201



if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    app.run(port=5004, debug=True, host='0.0.0.0')
