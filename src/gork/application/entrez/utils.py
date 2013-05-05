# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import entrez
#from entrez.models import EntrezEntry
from entrez.settings import ENTREZ_SEARCH_MAX


def get_current_date():
    return date(datetime.now().year, datetime.now().month, datetime.now().day)


def format_entrez_date(d):
    return '%s/%s/%s' % (d.year, d.month, d.day)


def convert_maxdate():
    d = date.today() - timedelta(days=1)
    return format_entrez_date(d)


def convert_mindate(d):
    return format_entrez_date(d)


def make_pubmed_entry(term, entry):
    e = entry[entry.find(' ')+1:].split('\n\n')
    abstract = e[-2].replace('\n', ' ')
    eid = e[-1][e[-1].find(' ')+1:e[-1].find('  ')]
    authors = e[2].replace('\n', ' ')
    title = e[1].replace('\n', ' ')
    magzine = e[0][e[0].find(' ')+1:].replace('\n', ' ')

    return EntrezEntry(
        content=entry,
        eid=eid,
        abstract=abstract,
        term=term,
        db=term.db,
        owner=term.owner,
        title=title,
        authors=authors,
        magzine=magzine
    )


def make_epigenomics_entry(term, entry):
    return EntrezEntry(
        content=entry,
        eid=entry,
        abstract='',
        term=term,
        db=term.db,
        owner=term.owner,
        title=entry,
        authors='',
        magzine=''
    )


def make_gene_entry(term, entry):
    e = entry[entry.find(' ')+1:].split('\n')
    abstract = e[1]
    eid = e[-1][e[-1].find(' ')+1:]
    authors = ''
    title = e[0]
    magzine = ''

    return EntrezEntry(
        content=entry,
        eid=eid,
        abstract=abstract,
        term=term,
        db=term.db,
        owner=term.owner,
        title=title,
        authors=authors,
        magzine=magzine
    )


def fetch_queryset(queryset):
    """
    Fetch EntrezEntry and save to database
    """
    for query in queryset:
        if query.lastedit_date >= get_current_date():
            continue

        entrez.email = query.owner.email

        if query.db == 'pubmed':
            datetype = 'edat'
            rettype = 'abstract'
            spliter = '\n\n\n'
            field = False
            make_entry = make_pubmed_entry
        elif query.db == 'epigenomics':
            datetype = 'pdat'
            rettype = False
            spliter = '\n'
            field = False
            make_entry = make_epigenomics_entry
        elif query.db == 'gene':
            datetype = 'pdat'
            rettype = False
            spliter = '\n\n'
            field = False
            make_entry = make_gene_entry

        handler = entrez.esearch(
            db=query.db,
            term=query.condition,
            retmax=ENTREZ_SEARCH_MAX,
            datetype=datetype,
            mindate=convert_mindate(query.lastedit_date),
            maxdate=convert_maxdate(),
            usehistory='y',
            field=field
        )
        result = entrez.read(handler)
        handler.close()

        if result['Count'] == '0':
            continue

        docs = entrez.efetch(
            db=query.db,
            id=','.join(result['IdList']),
            retmode='text',
            rettype=rettype
        ).read().strip('\n').split(spliter)

        EntrezEntry.objects.bulk_create([make_entry(query, doc) for doc in docs])

    queryset.update(lastedit_date=get_current_date())

'''
def switch(key):
    case = {
        'pubmed': lambda: pubmed(),
        'gene': lambda: gene(),
    }
    return case[key]()
'''
