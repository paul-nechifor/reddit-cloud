reddit-cloud
============

This is a Reddit bot which generates word clouds for comments in submissions.
I'm running it on user [WordCloudBot2][1].

Installation
------------

Install all the dependencies by using the `requirements.txt` file. Please note
that if you are using Mac OS X, you might have to install a Fortran compiler in
order to fulfill some dependencies.

    pip install -r requirements.txt

Copy the sample configuration file:

    cp config-sample.json config.json

### Notes

You are going to need a valid client id in order to upload the generated word cloud
to imgur, which you can get by [registering][3] an imgur application.

You can also place some OTF or TTF files in the `fonts` directory; and they will
be used to generate the word cloud.

### Usage

    python bot.py -h

Acknowledgements
----------------

* [Andreas Mueller][2]'s `word_cloud` library.

[1]:  http://www.reddit.com/user/WordCloudBot2
[2]:  https://github.com/amueller
[3]:  http://api.imgur.com/oauth2/addclient
