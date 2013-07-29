reddit-cloud
============

This is a Reddit bot which generates word clouds for comments in submissions.
I'm running it on user [WordCloudBot2][1].

Installation
------------

I am going to go on a limb and suggest that you should probably use [virtualenv][2],
in order to use this script.

Install the script's dependencies:

    pip install -r requirements.txt

Copy the sample configuration file:

    cp config-sample.json config.json

### Usage

    python bot.py -h

### Notes

If you are using Mac OS X, you might have to install a Fortran compiler in order
to fulfill some of the dependencies.

You are going to need a valid client id in order to upload the generated word
cloud image to imgur, which you can get by [registering][3] an imgur application.

You can also place some OTF or TTF files in the `fonts` directory; and they will
be used to generate the word cloud.

Acknowledgements
----------------

* [Andreas Mueller][4]'s `wordcloud` library.

[1]:  http://www.reddit.com/user/WordCloudBot2
[2]:  http://docs.python-guide.org/en/latest/dev/virtualenvs.html
[3]:  http://api.imgur.com/oauth2/addclient
[4]:  http://github.com/amueller/word_cloud
