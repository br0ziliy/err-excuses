# This is a skeleton for Err plugins, use this to get started quickly.

from errbot import BotPlugin, botcmd, webhook
import requests, json
from lxml import html

class Excuses(BotPlugin):
    """An Err plugin skeleton"""

    def _get_url_text(url):
        r = requests.get(url)
        if r.code == 200:
            return r.text

    def _get_qa():
        page = self._get_url_text('http://qaexcuses.com/')
        tree = html.fromstring(page)
        quote = tree.xpath('//a[1]/text()')
        return quote[0]

    def _get_devcom():
        page = self._get_url_text('http://developerexcuses.com/')
        tree = html.fromstring(page)
        quote = tree.xpath('//a[1]/text()')
        return quote[0]

    def _get_devru():
        page = self._get_url_text('http://developerexcuses.com/')
        for line in page.split('\n'):
            if line.lstrip.startswith('initial'):
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
        what = args[0]
        if not what: what = 'devcom'
        try:
            f = getattr(self,"_get_"+what)
        except AttributeError:
            return "cant do"
        return f()
