# gudlift-registration

1. Why

   This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

   This project uses the following technologies:

   - Python v3.x+

   - [Flask](https://flask.palletsprojects.com/en/1.1.x/)

     Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

   - [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

     This ensures you'll be able to install the correct packages without interfering with Python on your machine.

     Before you begin, please ensure you have this installed globally.

   - Convention Name
      For JsonFile => camelCase
      For Python => snake_case
   - Convention Language Python : PEP8

3. Installation

   - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

   - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

   - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

   - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

   - You should now be ready to test the application. In the directory, type either <code>export FLASK_APP=server </code> and after <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser. defaut: [http://127.0.0.1:5000](http://127.0.0.1:5000])

4. Current Setup

   The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:

   - competitions.json - list of competitions
   - clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.
   - booking.json - list of booking places by clubs for differentes dates/competitions.

5. Testing

   The test framework used is pytest for unit and integration tests as well as the [Selenium](https://selenium-python.readthedocs.io)  framework for functional tests.
   The [coverage](https://coverage.readthedocs.io/en/6.3.2/) framework is installed to know the coverage of the code under test with settings_file "setup.cfg".

   To run Pytest with tested code coverage: 
   <code>pytest --cov -v</code>

   To run Pytest with export report coverage HTML :
   <code>pytest --cov --cov-report html -v</code>

6. Perform

   The Locust framework has been configured to simulate reservations on the Flask application (6 users)
   <code>locust -f ./tests/performance_tests/locustfile.py</code>

   
