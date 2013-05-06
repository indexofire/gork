# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta


def get_current_date():
    return date(datetime.now().year, datetime.now().month, datetime.now().day)


def format_entrez_date(d):
    return '%s/%s/%s' % (d.year, d.month, d.day)


def convert_maxdate():
    d = date.today() - timedelta(days=1)
    return format_entrez_date(d)


def convert_mindate(d):
    return format_entrez_date(d)
