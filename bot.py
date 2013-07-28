#!/usr/bin/env python2
# coding: utf-8

import json, time, re, random, traceback, htmlentitydefs, os
import praw, numpy, pyimgur, wordcloud
from HTMLParser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer

def escapeHtml(what):
    return HTMLParser.unescape.__func__(HTMLParser, what)

def cleanComment(comment):
    html = escapeHtml(comment.body_html)
    cp = CommentParser()
    cp.feed(html)
    return cp.text

class CommentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ''
    def handle_data(self, data):
        self.text += data
    def handle_entityref(self, name):
        self.text += htmlentitydefs.entitydefs[name]
    def handle_charref(self, name):
        if name[0] == 'x':
            self.text += unichr(int(name[1:], 16))
        else:
            self.text += unichr(int(name))

class Client:
    def __init__(self, config):
        self.config = config
        self.replyPause = config['replyPause']
        self.size = config['size']
        self.scale = config['scale']
        self.reddit = praw.Reddit(config['userAgent'])
        self.respFile = 'respondedTo.json'
        if os.path.exists(self.respFile):
            resp = json.loads(open(self.respFile).read())
        else:
            resp = []
        self.respondedTo = set(resp)
        self.fonts = self.getFonts()
        self.outFile = 'out.png'

    def getFonts(self):
        fonts = []
        for f in os.listdir('fonts'):
            ext = f.split('.')[-1].lower()
            if ext in ('otf', 'ttf'):
                fonts.append('fonts/' + f)
        return fonts

    def start(self):
        self.reddit.login(self.config['username'], self.config['password'])
        self.loop()

    def loop(self):
        while True:
            try:
                submissions = self.getUnreplyedSubmissions()
                for s in submissions:
                    try:
                        self.generateCloudFor(s)
                        time.sleep(self.replyPause)
                    except:
                        traceback.print_exc()
                        time.sleep(self.replyPause)
                        continue
            except:
                traceback.print_exc()
            time.sleep(self.replyPause)

    def getUnreplyedSubmissions(self):
        submissions = self.reddit.get_subreddit('all').get_hot(limit=100)
        unreplyed = []

        for s in submissions:
            if s.id not in self.respondedTo:
                unreplyed.append(s)

        return unreplyed

    def generateCloudFor(self, submission):
        self.respondedTo.add(submission.id)
        out = open(self.respFile, 'w')
        out.write(json.dumps(list(self.respondedTo)))
        out.close()

        text = self.getSubmissionText(submission.id)
        self.makeCloud(text)
        url = self.uploadImage()
        comment = '[Word cloud out of all the comments.](%s)' % url
        comment += '\n\n' + self.config['signature']
        submission.add_comment(comment)
        print url

    def getSubmissionText(self, sid):
        sub = self.reddit.get_submission(submission_id=sid, comment_limit=None)
        flatComments = praw.helpers.flatten_tree(sub.comments)
        allText = ''
        for comment in flatComments:
            if isinstance(comment, praw.objects.Comment):
                allText += cleanComment(comment)
        return allText

    def makeCloud(self, text):
        font = random.choice(self.fonts)
        words, counts = wordcloud.process_text(text, max_features=2000)
        elements = wordcloud.fit_words(words, counts, width=self.size,
                height=self.size, font_path=font)
        wordcloud.draw(elements, self.outFile, width=self.size,
                height=self.size, scale=self.scale, font_path=font)

    def uploadImage(self):
        im = pyimgur.Imgur(self.config['clientId'])
        ui = im.upload_image(self.outFile)
        os.remove(self.outFile)

        return ui.link

def main():
    config = json.loads(open('config.json').read())

    c = Client(config)
    c.start()

if __name__ == '__main__':
    main()
