# Aban tether code challenge

this repo aims to solve the following challenge:

    Problem:

        Design an API for placing a purchase order from a cryptocurrency exchange with the following conditions:

        Each purchase should receive the following inputs:

        Cryptocurrency name for purchase (e.g., ABAN).
        Amount of cryptocurrency for purchase (e.g., 1).
        To perform the purchase operation, two tasks need to be accomplished:

        Deduct the money from the customer's account based on the price of the cryptocurrency and the amount purchased (for simplicity, you can hard code the prices).
        Clear the purchased amount with international exchanges (create an empty method named "buy_from_exchange" responsible for clearing the purchase. Assume this method sends an HTTP request to international exchanges).
        Since international exchanges do not support purchases under $10, the settlement for these orders should be done collectively with other orders under $10.

        Example:

        To better understand the problem, pay attention to the following examples (the price of cryptocurrency ABAN is $4 in all examples):

        You receive an order to purchase 3 ABAN cryptocurrencies. At the moment of receiving the request through the API, $12 should be deducted from the user's account, and the "buy_from_exchange" function should be called with arguments ABAN and 3.

        You receive 3 different orders from different users to purchase 1 ABAN cryptocurrency. At the moment of receiving each request through the API, only $4 should be deducted from the ordering user's account. However, the "buy_from_exchange" function should be called only once, after the last purchase (at the earliest possible time) with arguments ABAN and 12.

        Implementation Notes:

        The implementation language should be Python.

        Prioritize using the Django framework, but it is not mandatory.

        Choose the services (such as the database) according to your own discretion and based on the problem requirements.

        Code cleanliness is highly important.

        Code standardization (adhering to OOP, SOLID principles, etc.) is crucial.

        Code performance is important.

        Writing tests is a positive factor.

        Dockerizing the project is a positive factor.

## NOTES

    1 - We assume that the dabase is already seeded with relevant data and thus beside of requested API we didn't provide the facilities for inserting them.
    
    2 - This repository is not supposed to be a complete and bug free application, it aims to merely demonestrate a possible solution to the mentioned problem.
    
    3 - Many details are neglected or overlooked due to the specific focus of the repository.

    4 - In order to make a call to the remote exchange, you need to use celery worker and must subscribe it on the `buy_from_exchange` queue.