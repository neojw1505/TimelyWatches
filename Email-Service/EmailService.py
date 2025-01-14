from flask import Flask, request, jsonify
from flask_mail import Mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from invokes import invoke_http
# pip3 install flask flask-mail
from jinja2 import Environment, FileSystemLoader
import os
from flasgger import Swagger
# from db_config import set_database_uri
from datetime import datetime
from flask_cors import CORS

'''
API Endpoints:
1. POST /notification/sendEmail - sending a email to the receipient regarding update on his bid


PORT: 5104

'''
########## initiate flask ##########
app = Flask(__name__)  # initialize a flask application

CORS(app)
########## initiate swagger ##########
# Initialize flasgger
app.config['SWAGGER'] = {
    'title': 'email service microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Allows create and retrieve of notification. Additionally, it sends email to the user.'
}
swagger = Swagger(app)

########## declaring mail ##########

app.config['MAIL_SERVER']="smtp.office365.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME'] = "watchauctiononlineplatform@outlook.com"
app.config['MAIL_PASSWORD'] = "password@0000"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL']= True
mail=Mail(app)

########## notification customisation ##########
notification_header="Notification for item: "

subheader={
    "outbid":"Oh No! Hurry!", 
    "winandpayremind":"Congratulations!",
    "paysucess":"Payment success!",
    "rollbackandpayremind":"Congratulations!",
    "schedulesuccess":"Schedule success!",
    "auctionstartfail": "Fail to start Auction :( " ,
    "auctionstarted": "Auction has started!" ,
    "auctionendfail": " Fail to end Auction :(  " ,
    "auctionended": " Auction has ended! " ,
    "auctioncreated": "Auction has been created! "
}

briefMessage={
    "outbid":"Out bidded for item: ", 
    "winandpayremind":"Congratulations on winning the item: ",
    "paysucess":"Payment success for the item: ",
    "rollbackandpayremind":"Congratulations on winning the item: ",
    "schedulesuccess":"You have schedule a time slot to collect the item: ",
    "auctionstartfail": "There is an error in starting your auction for item: " ,
    "auctionstarted": "We have successfully started your auction for item: " ,
    "auctionendfail": " There is an error in ending your auction for item:  " ,
    "auctionended": " We have successfully ended your auction for item: " ,
    "auctioncreated": "We have successfully created your auction for item: "
    }

notification_body={
    "outbid":"The item that you have recently bidded for has been outbidded by an annoymous bidder. Do log into Timely Watches to place a higher bid.", 

    "winandpayremind":"Congratulation on winning the bid! Do log into Timely Watches and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.",

    "paysucess":"We have sucessfully receive your payment for the item. Do log into Timely Watches to schedule a timing for the collection of the watch! ",

    "rollbackandpayremind":"Congratulation on winning the bid! As the highest bidder has given up the offer, the item will be offered to you! Do log into Timely Watches and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.",

    "schedulesuccess":"Do take note of the allocated time that you have indicated for the item collection. Vist our website to check the collection point with the seller!",

    "auctionstartfail":"There seems to be an error starting the auction for your item mentioned above. Do log into our website to check on your auction. ",

    "auctionstarted":"Your auction for the following item has open successfully for users to bid for your item. We will send you another email to notify you when the auction has ended. ",

    "auctionendfail":" There seems to be an error ending the auction for your item mentioned above. Do log into our website to check on your auction. ",

    "auctionended":"Your auction for the following item has ended successfully. Do log into our website to check on your auction and the winner's bid!. ",

    "auctioncreated": "You have successfully created a new auction. Do log into our website to check on your auction and the winner's bid!."
}




"""
{
    "recipient": {
        "code": 200,
        "data": {
            "account_status": 1,
            "account_type": "customer",
            "address": "123 Street,City",
            "email": "kaijie.wang.2022@smu.edu.sg",
            "first_name": "Kaijie",
            "gender": "M",
            "id": 1,
            "last_name": "Wang",
            "password": "password",
            "phone_number": "1234567890",
            "profile_picture": "https://example.com/profile.jpg",
            "registration_date": "2024-02-24 10:19:27"
            }
        },
        "auction": {
            "code": 200,
            "data": {
                "auction_id": 1,
                "auction_item": "Watch",
                "current_price": 120.0,
                "end_time": "2024-02-23 12:00",
                "start_price": 100.0,
                "start_time": "2024-02-23 10:00"
                }
            },
        "type": "outbid",
        "schedule": {
            "code": 200,
            "data": {
                "auction_id": 1,
                "collection_time": "2024-03-25T10:00:00.000",
                "user_id": 1
            }
        }
    }"""

# POST /notification/sendEmail - sending a email to the receipient regarding update on his bid
@app.route('/emailservice/sendEmail', methods=['POST'])
def sendEmail():
    """
    Create a notification and send it to the user. the notification will be based on the notification type passed in the request body
    ---
    requestBody:
        description: notification creation detail
        required: true
        content:
            application/json:
                schema:
                    properties:
                        recipient:
                            type: object
                            properties:
                                code:
                                    type: integer
                                data:
                                    type: object
                                    properties:
                                        account_status:
                                            type: integer
                                        account_type:
                                            type: string
                                        address:
                                            type: string
                                        email:
                                            type: string
                                        first_name:
                                            type: string
                                        gender:
                                            type: string
                                        id:
                                            type: integer
                                        last_name:
                                            type: string
                                        password:
                                            type: string
                                        phone_number:
                                            type: string
                                        profile_picture:
                                            type: string
                                        registration_date:
                                            type: string
                                            format: date-time
                        auction:
                            type: object
                            properties:
                                code:
                                    type: integer
                                data:
                                    type: object
                                    properties:
                                        auction_id:
                                            type: integer
                                        auction_item:
                                            type: string
                                        current_price:
                                            type: number
                                        end_time:
                                            type: string
                                            format: date-time
                                        start_price:
                                            type: number
                                        start_time:
                                            type: string
                                            format: date-time
                        notification_type:
                            type: string

                        schedule:
                            type: object
                            properties:
                                code:
                                    type: integer
                                data:
                                    type: object
                                    properties:
                                        auction_id:
                                            type: integer
                                        collection_time:
                                            type: string
                                            format: date-time
                                        user_id:
                                            type: integer
                        

    responses:
        404:
            description: either user or auction does not exist

    """
    email_info = request.get_json()
    print(email_info)
    
    #creating the body of notification/email
    sender_email = "watchauctiononlineplatform@outlook.com"
    recipient_email =  email_info["recipient"]["data"]["email"]
    # print(recipient_email)
    subject = notification_header+email_info["auction"]["data"]["auction_item"]


    collectionDate,collectionTime="",""
    #changing schedule format
    print(email_info["schedule"])
    if email_info["schedule"]!="":
        print(email_info["schedule"]["data"]["collection_time"])

        date_string = email_info["schedule"]["data"]["collection_time"]
        dt_object = datetime.fromisoformat(date_string)
        # Format the datetime object in a human-readable format
        human_readable_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
        collectionDate,collectionTime= human_readable_date.split(" ")
        collectionDate="Date: "+collectionDate
        collectionTime="Time: "+collectionTime


    #content for email body 
    email_content = {
        "subheader": subheader[email_info["type"]],
        "auctionItem": email_info["auction"]["data"]["auction_item"],
        "briefMessage": briefMessage[email_info["type"]],
        "bodyMessage": notification_body[email_info["type"]],
        "scheduleDate":collectionDate,
        "scheduleTime":collectionTime
    }
    # print(email_content)

    ##config and render the email template 
    # Configure Jinja2
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))

    # Get the template
    template = env.get_template('confirmEmailTemplate.html')

    # Render the template with content
    html_content = template.render(**email_content)

    # Set up the SMTP server
    smtp_server = 'smtp-mail.outlook.com'
    port = 587
    username = "watchauctiononlineplatform@outlook.com" # Update with your Outlook email
    password = 'password@0000'  # Update with your Outlook password

    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("message has been sent successfully")
        return "message has been sent successfully"
    except Exception as e:
        print("Error in sending email")
        return 'Error: ' + str(e)


if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    app.run(port=5104, debug=True, host='0.0.0.0')
