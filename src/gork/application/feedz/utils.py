# -*- coding: utf-8 -*-
from urlparse import urlsplit
from lxml.html import tostring, fromstring, HTMLParser
from lxml.html.clean import Cleaner


def html_link(url):
    host = urlsplit(url).hostname
    return u'<a href="%s">%s</a>' % (url, host)


def render_html(node, encoding='utf-8', make_unicode=False):
    """
    Render Element node.
    """
    if make_unicode or encoding == 'unicode':
        return tostring(node, encoding='utf-8').decode('utf-8')
    else:
        return tostring(node, encoding=encoding)


def parse_html(html, encoding='utf-8'):
    """
    Parse html into ElementTree node.
    """
    parser = HTMLParser(encoding=encoding)
    return fromstring(html, parser=parser)


def clean_html(html, safe_attrs=('src', 'href'), encoding='utf-8'):
    """
    Fix HTML structure and remove non-allowed attributes from all tags.
    Return UTF-8 HTML.
    """

    # Conver HTML to Unicode
    html = render_html(parse_html(html, encoding=encoding), make_unicode=True)

    # Strip some shit with default lxml tools
    cleaner = Cleaner(page_structure=True)
    html = cleaner.clean_html(html)

    # Keep only allowed attributes
    tree = parse_html(html)
    for elem in tree.xpath('.//*'):
        for key in elem.attrib.keys():
            if key not in safe_attrs:
                del elem.attrib[key]

    return render_html(tree)
