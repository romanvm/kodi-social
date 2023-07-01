import feedparser

KODI_RSS = 'https://kodi.tv/rss.xml'


def get_posts():
    feed = feedparser.parse(KODI_RSS)
    entries = feed.entries
    entries.sort(key=lambda e: e['published_parsed'])
    return entries
