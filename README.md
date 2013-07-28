reddit-cloud
============

This is a Reddit bot which generates word clouds for comments in submissions.
I'm running it on user
[WordCloudBot2](http://www.reddit.com/user/WordCloudBot2).

Requirements
------------

You need PRAW for the Reddit API. Install it with:

    pip install praw

You need `pyimgur` in order to upload the images automatically to Imgur. You can
install it by:

    pip install pyimgur

but this might not work (it didn't for me on Ubuntu). You can install it from
GitHub by:

    wget https://github.com/Damgaard/PyImgur/archive/master.zip
    unzip master.zip
    cd PyImgur-master
    sudo python setup.py install
    cd ..
    sudo rm -r PyImgur-master master.zip

The next thing that's needed is my fork of
[Andreas Mueller](https://github.com/amueller)'s `word_cloud`. You can find it
at [word cloud](https://github.com/paul-nechifor/word_cloud). Install it as a
package by running:

    amuelle://github.com/paul-nechifor/word_cloud/archive/master.zip
    unzip master.zip
    cd word_cloud-master
    sudo python setup.py install
    cd ..
    sudo rm -r word_cloud-master master.zip

Running it
----------

You need to place some OTF or TTF files in `fonts` before running it and create
a `config.json` file (rename `config-sample.json` to `config.json` and edit it).
