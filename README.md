reddit-cloud
============

This is a Reddit bot which generates word clouds for comments in submissions.
I'm running it on user
[WordCloudeBot2](http://www.reddit.com/user/WordCloudBot2).

This uses `praw` for the Reddit API, `pyimgur` to upload images to Imgur and
[Andreas Mueller](https://github.com/amueller)'s
[word cloud](https://github.com/amueller/word_cloud) which is
[described](http://peekaboo-vision.blogspot.ro/2012/11/a-wordcloud-in-python.html) here.

Installing all the requirements is a bit dificult depending on the platform.

You need to place some OTF or TTF files in `fonts` before running it and create
a `config.json` file (rename `config-sample.json` to `config.json` and edit it).
