reddit-cloud
============

This is a Reddit bot which generates word clouds for comments in submissions.
I'm running it on user [WordCloudBot2][1]. You can read a [longer
description][2] on my blog. Skip down to the [instructions](#instructions) to
run it by yourself.

## Frequent questions and suggestions

1. **How does the bot operate?**  
It gets submissions from /r/all ordered by hot. It reads all the comments in
a submission, eliminates the common words, generates a word cloud, posts it to
Imgur and posts the link in that submission.

2. **Do the images update?**  
No. It would be impractical to revisit posts.

3. **The fonts are horrible and unreadable.**  
It's supposed to be more artistic than readable.

4. **This bot is bad. Does anybody like this?**  
Yes. [Some people think it's nice.][3] Please don't ban the bot if you're a mod.

5. **How are the word clouds generated? Where is that code?**  
That's not in the bot source. It uses [my fork][4] of Andreas Mueller's
[word_cloud][5]. It basically draws all words to a black and white canvas and
when a new word is added it checks if writing it there would intersect other
written pixels. You can imagine that intersecting complex font paths would be
way more intensive.

6. **Do you take requests?**  
I haven't written that do be done automatically, I probably should.


## Instructions

### Installation

I am going to go on a limb and suggest that you should probably use
[virtualenv][3] in order to use this script.

Install the script's dependencies:

    pip install -r requirements.txt

### Configuration

Copy the sample configuration file:

    cp config-sample.json config.json

You need to register a new Reddit account to use for your bot and change the
`username` and `password` fields in `config.json`.

Get an Imgur account and then [register][6] for an application. Put the client
ID you get in `clientId`.

### Fonts

Place any OTF or TTF font files in `fonts/`. Fonts are randomly chosen from
there when a word cloud is generated. Open Sans is included by default.

### Usage

You normally run the bot by:

    python bot.py hot

To post a word cloud of somebody's comments as a reply to a post do:

    python bot.py user-hist <username> <full-permalink-of-the-comment>

To view the help run:

    python bot.py -h

### Notes

If you are using Mac OS X, you might have to install a Fortran compiler in order
to fulfill some of the dependencies.

[1]: http://www.reddit.com/user/WordCloudBot2
[2]: http://blog.paul.nechifor.net/post/57349950225/word-cloud-bot-for-reddit
[3]: http://docs.python-guide.org/en/latest/dev/virtualenvs.html
[4]: https://github.com/paul-nechifor/word_cloud
[5]: https://github.com/amueller/word_cloud
[6]: http://api.imgur.com/oauth2/addclient
