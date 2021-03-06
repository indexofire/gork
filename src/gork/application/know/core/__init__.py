# -*- coding: utf-8 -*-
import markdown
from know.core.plugins import registry as plugin_registry
from know.conf import settings


class ArticleMarkdown(markdown.Markdown):
    def __init__(self, article, *args, **kwargs):
        kwargs = settings.MARKDOWN_KWARGS
        kwargs['extensions'] = kwargs.get('extensions', [])
        kwargs['extensions'] += plugin_registry.get_markdown_extensions()
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.article = article


def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)
