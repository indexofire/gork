# -*- coding: utf-8 -*-


class NoRootURL(Exception):
    """If no root URL is found, we raise this"""
    pass


class MultipleRootURLs(Exception):
    """If there is more than one"""
    pass
