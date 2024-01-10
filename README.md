# testbee
This is an API that can be used by employers and educational bodies to administer test by just typing their custom questions  in the question page. There are also questions made already for students who wish to test their knowledge on basic subjects. These subjects include the common Mathematics, English and Reasoning. It designed to be user-friendly and the score appears immediately the test taker clicks the submit button.
> ****Architecture and Technology**
In building this project: The technology used basically is python Flask. This microframework is what is used in the backend technology and also to serve static pages.
Jinja is used as the templating engine to transmit data from the flask to the html pages.
Flask-Admin was used to build the administrative interface on Flask since the users would need to login. There are two different kinds of login used in the product. There is a login as a student and as a facilitator. The facilitator has the privilege to customize questions and also see the people logged in while the student only has the privilege of seeing and answering the questions and nothing else.
The database used was SQL and SQLAlchemy is used as the Object Relational Mapper(ORM).
