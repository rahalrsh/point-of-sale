# Point of sale API
Project to design and implement an API for a point of sale (POS) system

# Installation
1) Create python3 virtual environment
```bash
python3 -m venv env && source env/bin/activate

pip3 install --upgrade pip
pip3 install -r requirements.txt
```

2) Init Database and run migrations
```bash
flask db init && flask db migrate && flask db upgrade
```

3) Start Flask application
```bash
flask run
```

4) You should see the below output after Step 3
```bash
* Running on http://127.0.0.1:5000/
```

# Run Unit Tests
To execute all the unit tests run this command

```bash
pytest tests/*
```

# API Endpoints
Below is a detailed description of all the API endpoints implemented\
Note: locally the Flask application will be running on http://127.0.0.1:5000/

1) Add a new Item to the system
```text
    URL: api/v1/items
    
    Method: POST
    
    Content Type: application/json
    
    Body:
        {
            "description": "Salad",
            "price": 12.5,
            "quantity": 20
        }
    
    Responses:
        200: Success. Item added
        400: Input validation error
        500: Internal server error
```

2) Get all items in the system
```text
    URL: api/v1/items
    
    Method: GET
    
    Content Type: application/json
    
    Body: N/A
    
    Responses:
        200: Success. All items returned
        404: No items found in the system
        500: Internal server error
```

3) Get an item by id
```text
    URL: api/v1/items/1
    
    Method: GET
    
    Content Type: application/json
    
    Body: N/A
    
    Responses:
        200: Success. Item found
        404: Item with item_id not found
        500: Internal server error
```

4) Update an item by id
```text
    URL: api/v1/items/1
    
    Method: PUT
    
    Content Type: application/json
    
    Body:
        {
        "description": "Pizza",
        "price": 22.5,
        "quantity": 10
    }
    
    Responses:
        200: Success. Item updated
        404: Item with item_id not found
        500: Internal server error
    """
```

5) Delete an item by id
```text
    URL: api/v1/items/1
    
    Method: DELETE
    
    Content Type: application/json
    
    Body: N/A
    
    Responses:
        200: Success. Item deleted
        404: Item with item_id not found
        500: Internal server error
```


6) Add a new Order to the system
```text
    URL: api/v1/orders
    
    Method: POST
    
    Content Type: application/json
    
    Body:
        {
            "order_items": [
                {
                    "item_id":1,
                    "order_quantity":1
                },
                {
                    "item_id":2,
                    "order_quantity":5
                }
            ],
            "payment_amount": 20.5,
            "order_note": "Add extra cheese"
        }
    
    Responses:
        200: Success. Order placed successfully
        400: Invalid payment error, ordered quantity not available or input validation error
        404: Ordered item(s) not found in the system
        500: Internal server error
```

7) Get an order by order id
```text
    URL: api/v1/orders/1
    
    Method: GET
    
    Content Type: application/json
    
    Body: N/A
    
    Responses:
        200: Success. Order found
        404: Order with order_id not found
        500: Internal server error
```
