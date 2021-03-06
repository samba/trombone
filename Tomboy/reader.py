from xml.dom import minidom 
import re, datetime

def getText(nodelist):
    result = []
    if isinstance(nodelist, minidom.Node):
        nodelist = nodelist.childNodes
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)


class Note(object):
    TOMBOY_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
    RE_TIME_TRAILER = re.compile(r'(\.[0-9]{6})[0-9]*([+-][0-9]{2}:?[0-9]{2})$')

    @classmethod
    def parseTimestamp(cls, timestamp):
        date = cls.RE_TIME_TRAILER.sub('\\1', timestamp)
        return datetime.datetime.strptime(date, cls.TOMBOY_TIME_FORMAT)

    def __init__(self, filename):
        self.tree = minidom.parse(filename)
        self.root = self.tree.documentElement

        assert self.root.tagName == 'note'
    
    @property
    def lastchange(self):
        return self.parseTimestamp(getText(self.root.getElementsByTagName('last-change-date')[0]))
        
    @property
    def created(self):
        return self.parseTimestamp(getText(self.root.getElementsByTagName('create-date')[0]))

    @property
    def title(self):
        return getText(self.root.getElementsByTagName('title')[0].childNodes).strip()

    @property
    def body_xml(self):
        return self.root.getElementsByTagName('note-content')[0]

    @property
    def body_html(self):
        xml = self.body_xml.cloneNode(True) # deep copy
        self.fixNode(xml)
        return xml

    @classmethod
    def fixNode(cls, node):
        if node.nodeType != node.ELEMENT_NODE:
            return node
        if node.tagName in ('note-content',):
            node.tagName = 'div'
            if node.hasAttribute('version'):
                node.removeAttribute('version')
        if node.tagName in ('list',):
            node.tagName = 'ul'
        if node.tagName in ('list-item',):
            node.tagName =  'li'
            if node.hasAttribute('dir'):
                node.removeAttribute('dir')
        if node.tagName in ('strikethrough',):
            node.tagName =  'strike'
        if node.tagName in ('bold', 'highlight',):
            node.tagName =  'b'
        if node.tagName in ('italic', 'datetime',):
            node.tagName =  'i'
        if node.tagName in ('underline',):
            node.tagName =  'u'
        if node.tagName in ('monospace',):
            node.tagName =  'tt'
        if node.tagName in ('link:internal', 'link:broken',):
            node.tagName =  'code'
        if node.tagName in ('link:external',):
            node.tagName =  'a'
            node.setAttribute('href', getText(node.childNodes))
        if node.tagName in ('link:url',):
            if getText(node.childNodes).startswith('http:') or \
                    getText(node.childNodes).startswith('https:') or \
                    getText(node.childNodes).startswith('ftp:'):
                node.tagName =  'a'
                node.setAttribute('href', getText(node.childNodes))
            else:
                node.tagName =  'b'
        if node.tagName.startswith('size:'):
            sizeStr = node.tagName[5:]
            node.tagName = 'font'
            if sizeStr is 'small':
                node.setAttribute('size', '-1')
            elif sizeStr is 'large':
                node.setAttribute('size', '+1')
            elif sizeStr is 'huge':
                node.setAttribute('size', '+2')

        for i in node.childNodes:
            if i.nodeType == i.ELEMENT_NODE:
                cls.fixNode(i)
        return node
        

