from invokes import invoke_http
import amqp_connection
import json
import pika
from os import environ;

'''
Functions (RabbitMQ)
1) receiveNotification- RabbitMQ consumer
2) callback(channel, method, properties, body)-function to call when there is a message published to notification
3) processNotif(recipient_id,auction_id,notification_type ) - process the notification received from the callback function 



scenario when user will receive the notification 
1) outbid- when someone out bidded the customer (highest bid changed). send to previous person with highest bid 
2) winandpayremind/rollbackandpayremind- when the person win the bid and it will tell the user to pay 
3) paysucess-notify user when payment is successful 
4) schedulesuccess - notifiy user about successful schedule of collection time
5) auctionstartfail - notify the seller when auction did not start successfully
6) auctionstarted - notify the seller when auction started successfully
7) auctionendfail - notify the seller when auction did not end successfully
8) auctionended - notify the seller when auction end successfully


'''
########## URL ##########
user_url=environ.get('user_url')  or 'http://localhost:5000/user'
auction_url=environ.get('auction_url') or 'http://localhost:5001/auction'
notification_url=environ.get('notification_url') or 'http://localhost:5004/notification'
schedule_url=environ.get('schedule_url') or 'http://localhost:5003/schedule'
emailservice_url=environ.get('emailservice_url')

########## For RabbitMQ ##########
e_queue_name = environ.get('a_queue_name') or 'Notification'

#1) receiveNotification- RabbitMQ consumer
def receiveNotification(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)
        print('Notification microservice: Consuming from queue:', e_queue_name)
        channel.start_consuming() # an implicit loop waiting to receive messages; 
        #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    except pika.exceptions.AMQPError as e:
        print(f"Notification microservice: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("Notification microservice: Program interrupted by user.")



"""
body json- 
{
    recipient_id: id
    auction_id: id
    notification_type: notif type (string)  <- must correspond to database shown above
}
"""
#2) callback(channel, method, properties, body)-function to call when there is a message published to notification
#this function create a log in notification database and send the email to user regarding specific message
def callback(channel, method, properties, body): 
    notif = json.loads(body) # notif will be in json format like the one in the docstring
    # print("--JSON:", notif)

    #log the notification into data
    createNotification_url=notification_url+"/createNotification"
    #checking if the user and auction exist
    specify_user_url= f"{user_url}/id/{notif["recipient_id"]}"
    user_response=invoke_http(specify_user_url,method="GET")

    specify_auction_url= f"{auction_url}/{notif["auction_id"]}"
    auction_response=invoke_http(specify_auction_url,method="GET")
    print(auction_response)
    print(user_response)

    if user_response["code"] not in range(200,300) or auction_response["code"] not in range(200,300):
        print("either user or auction does not exist")
        return
    
 

    notification_response=invoke_http(createNotification_url, method="POST",json=notif)
    
    if notification_response["code"] not in range(200,300):
        print(notification_response)
        print("unable to add into database")
        return
    
    #process to send the notiification to that email  
    processNotif(user_response, auction_response, notif)

#3) processNotif(recipient_id,auction_id,notification_type ) - process the notification received from the callback function 
def processNotif(user , auction, notif):
    print(notif)

        #account for schedule 
    schedule=""
    if "schedule_id" in notif:
        schedule_id=notif["schedule_id"]
        specify_schedule_url= f"{schedule_url}/{schedule_id}"
        schedule=invoke_http(specify_schedule_url,method="GET")
    
    email_info={
        "recipient":user,
        "auction":auction,
        "type":notif["notification_type"],
        "schedule":schedule
    }

    print("information:", email_info )
    #send user email and the notification body 
    send_email_url=emailservice_url+"/sendEmail"
    invoke_http(send_email_url,method='POST', json=email_info)
    print("email has been sent")
  

if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    print("Notification microservice: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("Notification microservice: Connection established successfully")
    channel = connection.channel()
    receiveNotification(channel)