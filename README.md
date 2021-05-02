# cafe-wifi-api
RESTful API build with Flask and SQLite that returns to the user data about cafes in London.

A RESTful API is simply an API (application program interface) which follows an architrectural style, REST, which stands for Representaional
State Transfer which is a subset of the HTTP protocol.

A web service which follows the guidelines of REST is therefore recognized as RESTful.

There are tons of guidelines for a RESTful architecture. However, the two main ones are:

1. The use of HTTP verbs
2. The use of specific patterns of routes/endpoint urls

The HTTP verbs used when making HTTP requests that are expected under a REST architecture are:
1.GET (which is similar to reading data from a database)
2.POST (which is similar to sending data or creating data to/in a database)
3.PUT (which consists of updating a an entire record)
4.PATCH (which consists of updating a part of a record)
5.DELETE (which consists of deleting a record)

The use of specific patterns or routes refers to the pre-determined role certain routes must play when it comes to the data the API is involved with.

![image](https://user-images.githubusercontent.com/55893421/116822055-cc647f80-ab4a-11eb-8024-dcec92763f15.png)

As we can see from this chart each route defined by an HTTP verbs has different role to play regarding the data, in this case, articles.

In our case, this API deals with a database of cafes and their relevant informations (if they have toilets, the wifi, etc..) as column fields.

One of the first challenge of this project was to serialize the data in the database (SQLAlchemy objects) into JSON format. For that purpose, we can use the 
Flask method jsonify(), but it is far more easier to just create a function which will serialise our database row Object to JSON by first converting it to 
a dictionary and then using jsonify() to convert the dictionary (which is very similar in structure to JSON) to a JSON. This far more adequate then to just simply 
use jsonify() and having to write all the code inside the jsonify() function.

![image](https://user-images.githubusercontent.com/55893421/116822329-49dcbf80-ab4c-11eb-9662-5f0e96f416c5.png)


While I was doing this project, I realized how much correlation there is between the role of these routes and the CRUD pattern of operations on database and how
each route implemented in Flask corresponded to a particular operation on database. This is highlighted in the comment.

A documentation for this API was generated using Postman (which was also used to test this API). 
The documentation can be found here: https://documenter.getpostman.com/view/11695119/TzK2bZpo

The user can make the requests described in the above documentation in order to get data about cafes in a JSON format.
