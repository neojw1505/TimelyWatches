import stripe
from flask import Flask, request, jsonify
from os import environ
from flasgger import Swagger
from flask_cors import CORS

stripe.api_key = "rk_test_51OrZSVC6Ev8NcoAAsL8tWKsJQRCKKCry61vycl0wbj3FrQkTJ4qs56KKb9AXwAyW63S6no13Rws6Ao5kLWBm504M00jybuhTVc"

app=Flask(__name__) 
CORS(app)

app.config["SWAGGER"] = {
    "title": "CreateAuction microservice API",
    "version": 1.0,
    "openapi": "3.0.2",
    "description": "Allows interaction with the CreateAuction complex microservice",
}

Swagger=Swagger(app)

@app.route('/stripe/create-stripe-product', methods=['POST'])
def create_stripe_product():
  """
    Create a stripe product link
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
                description: The item being auctioned
              auction_id:
                type: integer
                description: The auction id
              start_price:
                type: integer
                description: The starting price of the auction
    responses:
      201:
        description: Auction created
      400:
        description: Bad request
  """
  try:
      data = request.get_json()
      product = stripe.Product.create(
          name=data['auction_item'],
          type='good',
          description="Deposit for " + data['auction_item']
      )
      print("Product created:", product)

      # Store the product ID for later reference
      product_id = data['auction_id']
      deposit = int(data['start_price'] * 10)

      # Create a price for the product
      price = stripe.Price.create(
          unit_amount=deposit,
          currency="sgd",
          product=product.id,
      )

      print("Price created:", price)
      
      checkout_session = stripe.checkout.Session.create(
          payment_method_types=['card'],
          line_items=[
              {
                  'price': price.id,
                  'quantity': 1,
              },
          ],
          mode='payment',
          success_url='http://localhost:3000/schedule/' + str(product_id),
          cancel_url='http://localhost:3000/cancel'
      )

      print("Checkout link:", checkout_session.url)
      return checkout_session["url"]
  except Exception as e:
      print("Error in Stripe:", e)
      return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5101, debug=True)
