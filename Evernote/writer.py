from xml.dom import minidom
import re, datetime

class Note(object):
    title = None
    content = None
    lastchange = None
    created = None

    ENML_DATE = '%Y%m%dT%H%M%SZ'
    MODIFIED_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'

    def __init__(self, *a, **kw):
        for i, v in kw.iteritems():
            setattr(self, i, v)


    @property
    def output(self):
        content = self.content
        if isinstance(content, minidom.Node):
            content = content.toxml()

        create_time = self.created.strftime(self.ENML_DATE)
        update_time = self.lastchange.strftime(self.ENML_DATE)

        yield '<note>\n'
        yield '<title>' + self.title + '</title>\n'
        yield '<content><![CDATA['
        yield '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        yield '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n'
        yield '<en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">\n'
        yield content 
        yield '</en-note>]]></content>\n'
        yield '<created>' + create_time + '</created>\n'
        yield '<updated>' + update_time + '</updated>\n'
        yield '<note-attributes/>\n'
        yield '</note>\n'


class Collection(object):
    notes = []

    APPLICATION = 'PyEvernoteExport'
    APPLICATION_VERSION = 'PyEvernoteExport 0.1'
    ENML_DATE = '%Y%m%dT%H%M%SZ'

    def __init__(self, output_buffer):
        self.target = output_buffer
        self.notes = []

    def addNote(self, note):
        if isinstance(note, Note):
            self.notes.append(note)

    @property
    def output(self):
        yield '<?xml version="1.0" encoding="UTF-8"?>\n'
        yield '<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export2.dtd">\n'
        yield '<en-export export-date="{today}" version="{appversion}" application="{application}">\n'.format(
                today = datetime.datetime.now().strftime(self.ENML_DATE),
                application = self.APPLICATION,
                appversion = self.APPLICATION_VERSION
            )
        for note in self.notes:
            yield ''.join(list(note.output))
        yield '</en-export>'


    def save(self):
        print >>self.target, ''.join(list(self.output))
