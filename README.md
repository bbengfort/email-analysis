# Email Analysis [![Build Status][build_status_img]][build_status_page] #
**Analyzing email traffic with Python**

[![Tidal Wave][tidal_wave.jpg]][tidal_wave.jpg]

My company recently gave me the oppertunity to use [MineMyMail][minemymail] to perform an email-wide analysis of my correspondence. Being the data scientist I am, I decided to  run some quick analytics to figure out what was going on inside my email; after all, email is a latent social network that is constructed in real time. Being a good Python programmer, I decided to go the whole nine yards and create an application that would work with the CSV output from [MineMyMail][minemymail] and generate a statistical report with Jinja2. Being a good open source guy- I created integration tests with [Travis CI][travis], a well structured repository, and open sourced it on [Github][github]. This is the result.

## Usage ##

This package expects a CSV output from MineMyMail, you can find an example in the `fixtures` directory. The ordered fields for this CSV file are as follows:

* Email Address
* Display Name
* First Name
* Middle Name
* Last Name
* City
* Region
* Country
* Facebook Link
* Count
* First Seen
* Last Seen

Once you have obtained this file, simply run the Python script in the `bin` directory as follows:

    $ bin/m3stat analyze --output=report.html emails.csv

The output option is the path to where to write the HTML report (by default it will write it to the current working directory with the current timestamp). The only argument is the path to the CSV. To get more options and usage run:

    $ bin/m3stat --help

Note, it is highly recommended that you create a virtual environment using `virtualenv` and install the requirements found in the requirements.txt file before executing this script. If any requirements are not met, an `ImportError` will be raised by the script.

## TODO ##

1. Write setup.py script
2. Include screenshots of report in documentation

<!-- References -->
[build_status_img]: https://travis-ci.org/bbengfort/email-analysis.png?branch=master
[build_status_page]: https://travis-ci.org/bbengfort/email-analysis
[tidal_wave.jpg]: http://static3.wikia.nocookie.net/__cb20120726190147/superfriends/images/8/87/Tidal_wave.jpg
[minemymail]: https://minemymail.com/
[jinja2]: http://jinja.pocoo.org/docs/
[travis]: https://travis-ci.org/
[github]: https://github.com
