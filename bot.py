#!/usr/bin/env python2
# coding: utf-8

import json, time, re, random, traceback, htmlentitydefs, os, sys, argparse
import praw, numpy, pyimgur, wordcloud
from HTMLParser import HTMLParser

def escapeHtml(what):
    return HTMLParser.unescape.__func__(HTMLParser, what)
    
def appendToFile(name, text):
    f = open(name, 'a+')
    f.write(text)
    f.close()

def cleanComment(comment):
    html = escapeHtml(comment.body_html)
    cp = CommentParser()
    cp.feed(html)
    return cp.text

class CommentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ''
        self.aTags = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.aTags += 1
    def handle_endtag(self, tag):
        if tag == 'a':
            self.aTags -= 1
    def handle_data(self, data):
        if self.aTags > 0 and data.startswith('http'):
            pass
        else:
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
        self.minComments = config['minComments']
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

    def login(self):
        self.reddit.login(self.config['username'], self.config['password'])

    def loop(self):
        while True:
            try:
                for s in self.getGoodSubmissions():
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

    def getGoodSubmissions(self):
        for s in self.reddit.get_subreddit('all').get_hot(limit=100):
            if s.id not in self.respondedTo \
                    and s.num_comments >= self.minComments:
                yield s

    def generateCloudFor(self, submission):
        self.respondedTo.add(submission.id)
        # TODO: Fix this. My file is getting too big.
        out = open(self.respFile, 'w')
        out.write(json.dumps(list(self.respondedTo)))
        out.close()

        text = self.getSubmissionText(submission.id)
        self.makeCloud(text)
        url = self.uploadImage()
        comment = '[Word cloud out of all the comments.](%s)' % url
        comment += '\n\n' + self.config['signature']
        
        submission.add_comment(comment)
        print 'New cloud:', url

    def getSubmissionText(self, sid):
        sub = self.reddit.get_submission(submission_id=sid, comment_limit=None)
        flatComments = praw.helpers.flatten_tree(sub.comments)
        allText = ''
        for comment in flatComments:
            if isinstance(comment, praw.objects.Comment):
                allText += cleanComment(comment) + '\n'
        return allText

    def makeCloud(self, text, font=None):
        if font is None:
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
        
        # Write the URL of the image so it's not forgotten even if commenting
        # fails.
        appendToFile('images.txt', ui.link + '\n')

        return ui.link

def postUserHist(client, redditorName, replyComment, font=None):
    user = client.reddit.get_redditor(redditorName)

    nComments = 0
    markdownChars = 0
    allText = ''

    for comment in user.get_comments(limit=None):
        nComments += 1
        markdownChars += len(comment.body)
        allText += cleanComment(comment) + '\n'
        if nComments % 100 == 0:
            print 'Got comments: ', nComments
    client.makeCloud(allText, font=font)
    url = client.uploadImage()
    
    comment = '[Word cloud for %d comments of yours.](%s)' % (nComments, url)
    comment += " That's %.2f KB of Markdown, by the way." % \
            (markdownChars / 1000.0)
    if markdownChars > 1000000:
        comment += ' You should write a book.'
    if nComments == 1000:
        comment += ' (I cannot get more than 1000 comments of yours.)'
    comment += '\n\n' + client.config['signature']

    replyComment.reply(comment)

def userHist(args, config):
    client = Client(config)
    client.login()
    try:
        replyComment = client.reddit.get_submission(args.replyTo).comments[0]
    except:
        traceback.print_exc()
        print "Invalid reply URL or Reddit isn't working."
        exit(1)

    postUserHist(client, args.name, replyComment, font=args.font)

def hot(args, config):
    client = Client(config)
    client.login()
    client.loop()
    
def submission(args, config):
    client = Client(config)
    client.login()
    try:
        submission = client.reddit.get_submission(submission_id=args.subId)
        client.generateCloudFor(submission)
    except:
        traceback.print_exc()
        print "Bad data or Reddit isn't working."
        exit(1)

def main():
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_user_hist = subparsers.add_parser('user-hist',
            help='generate a word cloud for a given user\'s history')
    parser_user_hist.add_argument('name', type=str, help="the user's name")
    parser_user_hist.add_argument('replyTo', type=str,
            help='the full URL the comment to which to add the reply')
    parser_user_hist.add_argument('--font', type=str,
            help='the font to be used',
            default='fonts/open_sans_light.ttf')
    parser_user_hist.set_defaults(func=userHist)

    parser_hot = subparsers.add_parser('hot',
            help='generate word cloud for the most popular threads')
    parser_hot.set_defaults(func=hot)
    
    parser_submission = subparsers.add_parser('submission',
            help='generate a word cloud for a specific submission')
    parser_submission.add_argument('subId', type=str,
            help='the submission id, like "1s2mkq"')
    parser_submission.set_defaults(func=submission)

    config = json.loads(open('config.json').read())
    args = parser.parse_args()
    args.func(args, config)

if __name__ == '__main__':
    main()
