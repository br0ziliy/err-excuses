# This is a skeleton for Err plugins, use this to get started quickly.

from errbot import BotPlugin, botcmd, webhook
import requests, json
from lxml import html

class Excuses(BotPlugin):
    """An Err plugin skeleton"""

    def _get_url_text(self,url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None

    def _get_qa(self):
        page = self._get_url_text('http://qaexcuses.com/')
        if page:
            tree = html.fromstring(page)
            quote = tree.xpath('//a[1]/text()')
            return quote[0]

    def _get_devcom(self):
        page = self._get_url_text('http://developerexcuses.com/')
        if page:
            tree = html.fromstring(page)
            quote = tree.xpath('//a[1]/text()')
            return quote[0]

    def _get_devru(self):
        page = self._get_url_text('http://developerexcuses.com/')
        if page:
            for line in page.split('\n'):
                if line.lstrip().startswith('initial'):
                    json_data = json_loads(line.split('=')[1].rstrip(','))
                    quote = json_data['text']
            if quote:
                return quote
            else:
                return "Can't do"
    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def excuse(self, mess, args):
        try:
            what = args[0]
        except IndexError:
            what = "devcom"
        try:
            f = getattr(self,"_get_"+what)
        except AttributeError:
            return "cant do"
        return f()
