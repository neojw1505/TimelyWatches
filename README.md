# WatchesAuction

## Front End

-   To start the project:

-   Step 1: Navigate to watch_auction_frontend/timely-watches/
    cd watch_auction_frontend/timely-watches/

-   Step 2: npm install all requirements
    npm install

-   Step 3: npm run dev to run the front end
    npm run dev

## Back End

-   Step 1: Copy dotenv.txt file from the zip root folder into the same file path as the compose.yaml and rename the file into .env

-   Step 2: Go to the compose.yaml file then run the following code:
    docker compose up

-   Step 3: To connect to the database (not needed) you can use the SQL log in credentials in the dotenv.txt file. You can put these credentials into MySQLWorkbench to send requests to edit the DB.

## Model Seller Accounts (For timelywatches)

-   Username: watchauctiononlineplatform@gmail.com
-   Password: password@0000

## Model Buyer Account 1 (For timelywatches)

-   Username: kaijie.wang.2022@smu.edu.sg
-   Password: password1!

## Seller account (For GMail)

-   Username: watchauctiononlineplatform@gmail.com
-   Password: password@0000

## Notes on Auction DB

-   Auction Status of 0 means the auction is closed
-   Auction Status of 1 means the auction is open
-   Auction Status of 2 or more means the auction is closed
-   Auction status of -1 is No Winnner (roll back until no more bidders or no one bidded the auction)
-   Auction status of -2 means winner has paid for the auction

### How to test the application

-   You can use the provided seller user type account and create auctions and you can create a buyer user type account to test making of bids or use the provided buyer account
- The seller gmail account is shown to allow you to test that the email is sent out to the gmail

### Scenario 1

-   Log in using a seller account
-   Go to create auction
-   Add images and and click button to send the images to the S3 bucket
-   Fill up the reference number, watch brand, manufacture year minimally to test the price predictor
-   Click create auction to create the auction

-   TESTING
-   You can check the docker containers to see the processes running in the back end
-   Example: checking auctions-1 and auctions-2 , one of it would run the create auction showing that the Nginx works

### Scenario 2

-   Log in using a user account
-   Go to any open auction
-   Place a bid
-   Log in to another user account
-   Place a bid

-   TESTING
-   You can see that there is a notification sent out when you get outbidded
-   An email is sent to show that you are outbidded
-   Watch auction bid price updates live as people bid

### Scenario 3

-   Log in to a user account
-   Use a PUT request to change the timing of the auction closing
-   Check the notifcation and email to see that you are the winner of the auction
-   You can make a PUT request to make the auction end 1h before the current time to test rollback
-   Auction status will change and the winner of the auction will be changed to the next highest bidder
