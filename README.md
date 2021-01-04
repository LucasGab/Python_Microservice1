# Python_Monolithic
 A proof of concept of a microservice architecture written in python and using flask and json.
 Simulate a simple library system.
 
Exercise response of course in Digital Innovation One: Fundamentals of systems architecture ("Fundamentos de arquitetura de sistemas") - module: Architectural concepts in Internet applications ("Conceitos de arquitetura em aplicações para Internet"), class taught by [Jefferson Stachelski](https://github.com/jeffhsta).
Exercises: https://github.com/jeffhsta/fundamentos_arquitetura

Each service runs in one port.
Has a simple automatic id system creation.

Architecture based Example (not equals, just simulates the interactions and comunication workflow):

![Microservice 1](https://raw.githubusercontent.com/LucasGab/Python_Microservice1/master/microservice1.png)

# Instruction

1. Clone the repository.
2. Needs Python 3.* .
3. Initiate a new `virtualenv venv` and install the `requirements.txt`.
4. Run the main.py and use a tool like postman to make the requests.


# End Points
    
    Users Service (Port=5000):

    GET /users : Return All Users list
        body: Nothing
    POST /users : Create User
        body:
        {
            "FirstName": "James",
            "LastName": "Bond",
            "Email":"JamesBond@Email.com"
        }

    PUT /users/<user_id> : Update User
        body:
        {
            "FirstName": "James",
            "LastName": "Bondeee",
            "Email":"JamesBond@Email.com"
        }

    GET /users/<user_id> : Get User Data
        body: Nothing
    DELETE /users/<user_id> : Delete User,
        body: Nothing

    Locations Module (Port=5001):

    GET /books : Return All Books list
        body: Nothing
    POST /books : Create Book
        body:
        {
            "Name":"Scrum",
            "Authors":["Jeff Sutherland","J. J. Sutherland"],
            "Quantity": 10,
            "UsersLocations": []
        }

    PUT /books/<book_id> : Update Book
        body:
        {
            "Name":"Scrum",
            "Authors":["Jeff Sutherland","J. J. Sutherland"],
            "Quantity": 5,
            "UsersLocations": []
        }

    GET /books/<book_id> : Get Book Data
        body: Nothing
    GET /books/users/<user_id> : Get User Books Id's
        body: Nothing
    DELETE /books/<book_id> : Delete Book
        body: Nothing
    POST /books/take/<book_id>/<user_id>: User takes a specific book
        body: Nothing
    POST /books/vacate/<book_id>/<user_id>: User vacate a book
        body: Nothing

    Reports Service (Port=5002):
    
    GET /reports/<user_id> : Get User Report
        body: Nothing
