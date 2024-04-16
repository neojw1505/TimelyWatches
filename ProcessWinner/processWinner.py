from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from invokes import invoke_http
import amqp_connection
import pika
import json
from os import environ
import pytz

##################  urls  ##################
auction_url=environ.get('auction_url') or 'http://localhost:5001/auction'
bids_url=environ.get('bids_url') or 'http://localhost:5002/bid'

app = Flask(__name__)
# timezone = pytz.timezone("Asia/Shanghai")

connection = amqp_connection.create_connection()
channel = connection.channel()

def check_auctions():
  # Check if the datetime matches the current time
  # If it does, call the process() function
    
  timezone = pytz.timezone("Asia/Shanghai")
  current_time = datetime.now(timezone)

  # Convert to offset-naive datetime object
  current_time = current_time.replace(tzinfo=None)
  print("Checking auctions at: ", current_time)
  try:
    auctions = invoke_http(auction_url, "get")
    processAuctions(auctions)
  except Exception as e:
    print("Error in checking auctions", e)

def processAuctions(auctions): 
  timezone = pytz.timezone("Asia/Shanghai")
  current_time = datetime.now(timezone)

  # Convert to offset-naive datetime object
  current_time = current_time.replace(tzinfo=None)
  # check if auctions status code is 200
  if auctions['code'] != 200:
    print("Error in auction microserivce, unable to retrieve auction data")
    # return status code 401
    return "Error in auction microserivce, unable to retrieve auction data" ,401
  
  else:

    for auction in auctions['data']['auctions']:
      auction_id = auction['auction_id']

      #convert time into readable format
      end_time = datetime.strptime(auction['end_time'], '%Y-%m-%d %H:%M:%S')
      start_time = datetime.strptime(auction['start_time'], '%Y-%m-%d %H:%M:%S')
      # if auction started then change status from 0 to 1
      if start_time <= current_time and current_time < end_time:
        # send put request to change status of auction from 0 to 1 to show that auction has started
        if auction['auction_status'] == 0:
          print("Auction", auction_id ,"started at: ", current_time)
          auction['auction_status'] = 1
          uri = auction_url + "/" + str(auction_id)
          auction_copy = auction.copy()
          del auction_copy['auction_id']
          update_status = invoke_http(uri, "PUT", json=auction_copy)

          # error handling for the put request
          if update_status['code'] != 200:
            print("Auction", auction_id, "has failed to update status from 0 to 1")
            email_seller("auctionstartfail", auction)
            pass
          else:
            print("Auction", auction_id, "has had its status updated from 0 to 1")
            email_seller("auctionstarted", auction)
            pass

      # if auction ended then change status from 1 to 2 and process the top bidder (switch the if statements)
      # elif end_time <= datetime.now(): #? for testing purposes can use this if statement instead
      elif current_time >= end_time: 
        # send put request to change status of auction from 1 to 2 to show that auction has ended
        if auction['auction_status'] == 1:
          print("Auction", auction_id ,"ended at: ", current_time)
          # process the top bidder of the auctionl
          winner_exist = process(auction)
          if winner_exist:
            auction['auction_status'] = 2
            uri = auction_url + "/" + str(auction_id) 
            auction_copy = auction.copy()
            del auction_copy['auction_id']
            try:
              update_status = invoke_http(uri, "PUT", json=auction_copy)
              if update_status['code'] != 200:
                print("Auction", auction_id, "has failed to update status from 1 to 2")
                email_seller("auctionendfail", auction)
              else:
                print("Auction", auction_id, "has had its status updated from 1 to 2")
                email_seller("auctionended", auction)
            except Exception as e:
              print("Error in updating auction status:", e)

            # update_status = invoke_http(uri, "PUT", json=auction_copy)
            # if update_status['code'] != 200:
            #   print("Auction", auction_id, "has failed to update status from 1 to 2")
            #   email_seller("auctionendfail", auction)
            # else:
            #   print("Auction", auction_id, "has had its status updated from 1 to 2")
            #   email_seller("auctionended", auction)
          else: 
            pass
      if auction['auction_status'] >= 2:
        hours_passed = (current_time - end_time).total_seconds() // 3600
        if hours_passed > (auction['auction_status'] - 2):
          print("Auction", auction_id ,"has been ended for", hours_passed, "hours")
          new_winner = rollback(auction)
          # Update auction status to reflect the number of hours that have passed
          auction['auction_status'] = hours_passed + 2 
          uri = auction_url + "/" + str(auction_id)
          auction_copy = auction.copy()
          auction_copy['auction_status'] = hours_passed + 2
          auction_copy["auction_winner_id"] = new_winner
          if new_winner == None:
            auction_copy["auction_status"] = -1
          del auction_copy['auction_id']
          try:
              update_status = invoke_http(uri, "PUT", json=auction_copy)
              if update_status['code'] != 200:
                print("Auction", auction_id, "has failed to update its status")
                email_seller("auctionendfail", auction)
              else:
                print("Auction", auction_id, "has had its status updated from", hours_passed + 1, "to", hours_passed + 2)
                email_seller("auctionended", auction)
          except Exception as e:
            print("Error in updating auction status:", e)
          # update_status = invoke_http(uri, "PUT", json=auction_copy)
          # # error handling for the put request
          # if update_status['code'] != 200:
          #   print("Auction", auction_id, "has failed to update status to reflect the number of hours that have passed")
          #   pass
          # else:
          #   print("Auction", auction_id, "has had its status updated to reflect the number of hours that have passed")
          # # Perform the desired action for the multiple of hours
          # pass

        # case where auction is still ongoing
        # pass 


def process(auction):
  exchangename = "notification_direct" 

  # check if there is a winner
  if auction['auction_winner_id'] != None:
    print("Winner for", auction['auction_id'] ,"is", auction['auction_winner_id'])
    # call AMQP to send a message to the winner
    message = {
      "recipient_id": auction['auction_winner_id'],
      "auction_id": auction['auction_id'],
      "notification_type": "winandpayremind"
    }
    message = json.dumps(message)
    channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")
    return True
  else:
    print(auction['auction_id'], "has no winner")
    # call AMQP to send a message to the seller
    # update auction status to reflect that there is no winner by changing status to -1
    auction['auction_status'] = -1
    uri = auction_url + "/" + str(auction['auction_id'])
    auction_copy = auction.copy()
    del auction_copy['auction_id']
    update_status = invoke_http(uri, "PUT", json=auction_copy)
    # email_seller("nowinner", auction)
    return False


def rollback(auction):
  # find the next highest bidder for the auction

  # invoke http for bids database for this auction
  auction_id = auction['auction_id']
  n_highiest_bidder = auction['auction_status'] - 2
  n_highiest_bidder = int(n_highiest_bidder)

  uri = f"{bids_url}/auction" + "/" + str(auction_id)
  bids = invoke_http(uri, "get")
  if bids['code'] == 200:
    # sort the bids in descending order
    sorted_bids = sorted(bids['data'], key=lambda k: k['bid_amount'], reverse=True)
    # get the next highest bidder

    # check if there is a next highest bidder
    if len(sorted_bids) <= n_highiest_bidder:
      print("There is no next highest bidder for auction", auction['auction_id'])

      # update auction status to -1 to show that there is no winner
      auction['auction_status'] = -1
      uri = auction_url + "/" + str(auction['auction_id'])
      auction_copy = auction.copy()
      del auction_copy['auction_id']
      update_status = invoke_http(uri, "PUT", json=auction_copy)

      # email_seller("nowinner", auction)
      return None
    else: 
      next_highest_bidder = sorted_bids[n_highiest_bidder]
      exchangename = "notification_direct"
      print("Winner for", auction['auction_id'], "has been rolled back to the", (n_highiest_bidder + 1) , "highest bidder, which is user id", next_highest_bidder['user_id'])
      # use notification to inform next highest bidder that they need to pay
      message = {
        "recipient_id": next_highest_bidder['user_id'],
        "auction_id": auction['auction_id'],
        "notification_type": "rollbackandpayremind"
      }
      message = json.dumps(message)
      channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")
      return next_highest_bidder["user_id"]
  else:
    #inform seller via email that the next highest bidder could not be found due to an error in Bids microservice
    print("Error in Bids microservice when trying to find the next highest bidder for auction", auction['auction_id'])
    # email_seller("rollbackfail", auction)
    return None


def email_seller(notification_type, auction):
  #?need to ensure new notification types is added to the notification_direct exchange
  exchangename = "notification_direct" 
  seller_id = 28  #! REPLACE with the actual seller id
  message = {
    "recipient_id": seller_id,
    "auction_id": auction['auction_id'],
    "notification_type": notification_type #! REPLACE with the actual notification type
  }
  message = json.dumps(message)
  channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(check_auctions, 'interval', seconds=5)  # Run the code every 5 seconds
  scheduler.start()
  app.run(port=5005, debug=True)
