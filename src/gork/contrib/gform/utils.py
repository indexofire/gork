# -*- codingL utf-8 -*-
import csv
import json
import codecs
import cStringIO
from decimal import Decimal


class JSONFieldDescriptor(object):
    """
    Descriptor for JSON Field
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, objtype):
        cache_field = '_cached_jsonfield_%s' % self.field
        if not hasattr(obj, cache_field):
            try:
                setattr(obj, cache_field, json.loads(getattr(obj, self.field), parse_float=Decimal))
            except (TypeError, ValueError):
                setattr(obj, cache_field, {})
        return getattr(obj, cache_field)

    def __set__(self, obj, value):
        setattr(obj, '_cached_jsonfield_%s' % self.field, value)
        setattr(obj, self.field, json.dumps(value, cls=json.JSONEncoder))


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        row = [unicode(s) for s in row]
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
