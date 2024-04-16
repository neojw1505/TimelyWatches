from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flasgger import Swagger
from os import environ
import amqp_connection
import pika
import json

app = Flask(__name__)
CORS(app)

app.config["SWAGGER"] = {
    "title": "CreateAuction microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows interaction with the CreateAuction complex microservice",
}
swagger = Swagger(app)

########## URL ##########
auction_url=environ.get('auction_url') or 'http://localhost:5001/auction'
schedule_url=environ.get('schedule_url') or 'http://localhost:5003/schedule'
stripe_url=environ.get('stripe_url') or 'http://localhost:5101/stripe'

connection = amqp_connection.create_connection()
channel = connection.channel()

def email_seller(notification_type, auction):
  #?need to ensure new notification types is added to the notification_direct exchange
  exchangename = "notification_direct" 
  seller_id = 22  #! REPLACE with the actual seller id
  message = {
    "recipient_id": seller_id,
    "auction_id": auction['auction_id'],
    "notification_type": notification_type #! REPLACE with the actual notification type
  }
  message = json.dumps(message)
  channel.basic_publish(exchange=exchangename, body=message, properties=pika.BasicProperties(delivery_mode = 2),routing_key="Notification")


@app.route('/createAuction', methods=['POST'])
def createAuction():
    """
    Create auction and schedule for the new item
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema: 
            type: object
            properties:
              auction_item:
                  type: string
                  description: The item being auctioned.
              start_time:
                type: string
                description: The start time of the auction in this format 2024-03-30 13:33.
              end_time:
                type: string
                description: The end time of the auction in this format 2024-03-30 13:33.
              start_price:
                type: number
                description: The starting price of the auction.
              current_price:
                type: number
                description: The current price of the auction.
              auction_winner_id:
                type: integer
                nullable: true
                description: The ID of the auction winner.
              auction_status:
                type: integer
                description: The status of the auction (0 = unopened, 1 = active, 2 = closed, -1 = no winner, -2 = winner has paid.).
              watch_ref:
                type: string
                description: The reference number of the watch.
              watch_condition:
                type: string
                description: The condition of the watch (e.g., new, used, like new).
              watch_brand:
                type: string
                description: The brand of the watch.
              watch_box_present:
                type: boolean
                description: Whether the watch box is present.
              watch_papers_present:
                type: boolean
                description: Whether the watch papers are present.
              watch_image1:
                type: string
                description: URL of image1
              watch_image2:
                type: string
                description: URL of image2
              watch_image3:
                type: string
                description: URL of image3
              manufacture_year:
                type: integer
                description: The year of the watch.
    responses:
        201:
            description: Auction and Schedule Created
        401:
            description: Error in Auction microservice
        402:
            description: Error in Schedule microservice
    """

    data = request.json
    auction_item = data.get('auction_item')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    start_price = data.get('start_price')
    # start_price = 0
    # current_price = data.get('current_price')
    current_price = 0
    auction_winner_id = None
    auction_status = 0
    watch_ref = data.get('watch_ref')
    watch_condition = data.get('watch_condition')
    watch_brand = data.get('watch_brand')
    watch_box_present = data.get('watch_box_present')
    watch_papers_present = data.get('watch_papers_present')
    watch_image1 = data.get('watch_image1')
    watch_image2 = data.get('watch_image2')
    watch_image3 = data.get('watch_image3')
    manufacture_year = data.get('manufacture_year')

    try: 
      auction_response = requests.post(
          auction_url,
          json={
              "auction_item": auction_item,
              "start_time": start_time,
              "end_time": end_time,
              "start_price": start_price,
              "current_price": current_price,
              "auction_winner_id": auction_winner_id,
              "auction_status": auction_status,
              "watch_ref": watch_ref,
              "watch_condition": watch_condition,
              "watch_brand": watch_brand,
              "watch_box_present": watch_box_present,
              "watch_papers_present": watch_papers_present,
              "watch_image1": watch_image1,
              "watch_image2": watch_image2,
              "watch_image3": watch_image3,
              "manufacture_year": manufacture_year,
          },
      )
      if (auction_response.status_code == 201):
          # auction_id = auction_response.data['auction_id']
          auction_data = auction_response.json()
          auction_id = auction_data['data']['auction_id']
          try:
            schedule_response = requests.post(
              f"{schedule_url}/create/{auction_id}"
            )
            if schedule_response.status_code == 201:
              email_seller("auctioncreated", auction_data['data'])
              try:
                print(auction_item, auction_id, start_price)
                create_stripe_product_response = requests.post(
                  f"{stripe_url}/create-stripe-product",

                  json={
                    "auction_item": auction_item,
                    "auction_id": auction_id,
                    "start_price": start_price
                  })
                  # get the response from create stripe product response and uppdate auction stripe product id
                try:
                  print(create_stripe_product_response.text)
                  auction_data['data']['stripe_product_id'] = create_stripe_product_response.text
                  auction_response = requests.put(
                    f"{auction_url}/{auction_id}",
                    json=auction_data['data']
                  )
                  if auction_response.status_code == 200:
                    return jsonify(
                      {
                        "code": 201,
                        "message": "Auction and Schedule Created",
                      }
                    ), 201
                  else:
                    return jsonify(
                      {
                        "code": 400,
                        "message": "Error updating auction with stripe product id"
                      }
                    ), 400
                except requests.exceptions.RequestException as e:
                  # handle request exception
                  return jsonify(
                    {
                      "code": 400,
                      "message": "Cannot reach Stripe microservice",
                      "stripe_message": e
                    }
                  ), 400
                  
              except requests.exceptions.RequestException as e:
                # handle request exception
                return jsonify(
                  {
                    "code": 400,
                    "message": "Cannot reach Stripe microservice",
                    "stripe_message": e
                  }
                ), 400
              # return jsonify(
              #   {
              #     "code": 201,
              #     "message": "Auction and Schedule Created",
              #   }
              # ), 201
            else:
              # handle schedule creation error
              return jsonify(
                {
                  "code": 400,
                  "message": "Error creating schedule in the Schedule microservice"
                }
              ), 400
          except requests.exceptions.RequestException as e:
            # handle request exception
            return jsonify(
              {
                "code": 400,
                "message": "Cannot reach Schedule microservice"
              }
            ), 400
      else:
          # handle auction creation error
          return jsonify(
              {
                  "code": 400,
                  "message": "Error creating auction in the Auctions microservice"
              }
          ), 400
    except requests.exceptions.RequestException as e:
      # handle request exception
      return jsonify(
        {
          "code": 400,
          "message": "Cannot reach Auction microservice"
        }
      ), 400
    #     if (schedule_response.status_code == 201):
    #         return jsonify(
    #             {
    #                 "code": 201,
    #                 "message": "Auction and Schedule Created",
    #             }
    #         ), 201
    #     else:
    #         # handle schedule creation error
    #         return jsonify(
    #             {
    #                 "code": 402,
    #                 "message": "Error creating schedule in the Schedule microservice"
    #             }
    #         ), schedule_response.status_code

    # else:
    #     # handle auction creation error
    #     return jsonify(
    #         {
    #             "code": 401,
    #             "message": "Error creating auction in the Auctions microservice"
    #         }
    #     ), auction_response.status_code


if __name__ == '__main__':
    app.run(port=5010, debug=True, host="0.0.0.0")
