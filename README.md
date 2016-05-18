# SMS Two Factor Authentication with Flask
[![Build Status](https://travis-ci.org/TwilioDevEd/sms2fa-flask.svg?branch=master)](https://travis-ci.org/TwilioDevEd/sms2fa-flask)

## Local development

This project is built using the [Flask](http://flask.pocoo.org/) web framework.

1. Clone this repository and `cd` into it.

1. Create a new virtual environment.
    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```
        virtualenv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```
        mkvirtualenv automated-survey
        ```

1. Install the requirements.

    ```
    pip install -r requirements.txt
    ```


1. Copy the sample configuration file and edit it to match your configuration.

  ```bash
  $ cp .env.example .env
  ```

 You can find your `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` in your
 [Twilio Account Settings](https://www.twilio.com/user/account/settings).
 You will also need a `TWILIO_NUMBER` that you may find [here](https://www.twilio.com/user/account/phone-numbers/incoming).

 Run `source .env` to export the environment variables.

1. Run the migrations.

    Our app uses SQLite, so you probably will not need to install additional software.

    ```
    python manage.py db upgrade
    ```

1. Start the development server.

    ```
    python manage.py runserver
    ```
    
1. Check it out at: [http://localhost:5000/](http://localhost:5000/).


That's it!

## Running the tests

You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

1. Run the tests.

    ```
    $ coverage run manage.py test
    ```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.


## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.
