import json
import xml.etree.ElementTree as ET
from optparse import OptionParser

def parse_tree(xml_file):
    return ET.parse(xml_file)

def tree_root(tree):
    return tree.getroot()

def parse_root(root):
    """
    Take the root and return sub Elements if found
    """

    front = root.find('front')
    body = root.find('body')
    back = root.find('back')
    sub_article = root.findall('sub-article')

    return front, body, back, sub_article

def parse_front(root):
    """
    front sub Elements
    """

    journal_meta = root.find('journal-meta')
    article_meta = root.find('article-meta')

    return journal_meta, article_meta

def parse_article_meta(root):
    """
    article-meta sub Elements
    TODO: check for when there are single or multiple elements in the DTD
    """

    abstract = root.findall('abstract')
    article_categories = root.findall('article-categories')
    article_id = root.findall('article-id')
    author_notes = root.findall('author-notes')
    contrib_group = root.findall('contrib-group')
    custom_meta_group = root.findall('custom-meta-group')
    elocation_id = root.findall('elocation-id')
    funding_group = root.findall('funding-group')
    history = root.findall('history')
    kwd_group = root.findall('kwd-group')
    permissions = root.findall('permissions')
    pub_date = root.findall('pub-date')
    related_article = root.findall('related-article')
    self_uri = root.findall('self-uri')
    title_group = root.findall('title-group')
    volume = root.findall('volume')

    return (abstract, article_categories, article_id, author_notes,
            contrib_group, custom_meta_group, elocation_id,
            funding_group, history, kwd_group, permissions,
            pub_date, related_article, self_uri, title_group, volume)

def parse_name(root):
    """
    name sub Elements
    """

    surname = root.find('surname')
    given_names = root.find('given-names')

    return surname, given_names

def parse_date(root):
    """
    date sub Elements
    """

    day = root.find('day')
    month = root.find('month')
    year = root.find('year')

    return day, month, year

def parse_history(root):
    """
    history sub Elements
    """

    date = root.find('date')
    return date

def parse_funding_group(root):
    """
    funding-group sub Elements
    """

    award_group = root.findall('award-group')
    funding_statement = root.findall('funding-statement')

    return award_group, funding_statement

def parse_award_group(root):
    """
    funding-group award-group sub Elements
    """
    
    funding_source = root.find('funding-source')
    award_id = root.find('award-id')
    principal_award_recipient = root.find('principal-award-recipient')

    return funding_source, award_id, principal_award_recipient

def debug_print(root):
    """
    Debug
    """

    print 'Object: '
    print root
    print "\n"

    print 'DOCTYPE: ' + '?????'
    print 'Root tag: ' + str(root.tag)
    print 'Root attrib: ' + str(root.attrib)

    print "\nChildren:\n"
    for child in root:
        print child.tag, child.attrib

    front, body, back, sub_article = parse_root(root)

    print "\nChildren of front:\n"
    for child in front:
        print child.tag, child.attrib

    journal_meta, article_meta = parse_front(front)

    # article-meta
    print "\nChildren of article-meta: "
    print "List length: " + str(len(article_meta)) + "\n"
    for child in article_meta:
        print child.tag, child.attrib

    (abstract, article_categories, article_id, author_notes, contrib_group,
     custom_meta_group, elocation_id, funding_group, history, kwd_group,
     permissions, pub_date, related_article, self_uri,
     title_group, volume) = parse_article_meta(article_meta)

    print "\nChildren of article-meta pub-date: "
    for child in pub_date:
        print "\npub-date pub-type = " + child.attrib["pub-type"]
        day, month, year = parse_date(child)
        for elem in day, month, year:
            if elem is not None:
                print elem.tag + " = " + elem.text

    print "\nChildren of history: "
    print "List length: " + str(len(history)) + "\n"
    for child in history:
        date = parse_history(child)
        print "\nChildren of date: "
        print "List length: " + str(len(date)) + "\n"
        print "\nhistory date date-type = " + date.attrib["date-type"]
        day, month, year = parse_date(date)
        for elem in day, month, year:
            if elem is not None:
                print elem.tag + " = " + elem.text

    print "\nChildren of article-meta funding-group: "
    for child in funding_group:
        for c2 in child:
            print c2.tag, c2.attrib
    award_group, funding_statement = parse_funding_group(child)
    for child in funding_statement:
        print child.text
    for child in award_group:
        print "\n" + "id = " + child.attrib["id"]
        (funding_source, award_id,
         principal_award_recipient) = parse_award_group(child)
        if funding_source:
            print "funding-source = " + funding_source.text
        if award_id:
            print "award-id = " + str(award_id.text)
        for name in principal_award_recipient:
            print "principal-award-recipient:"
            surname, given_names = parse_name(name)
            print "  surname = " + surname.text
            print "  given-names = " + str(given_names.text)

    # sub-article
    print "\nChildren of sub-article: "
    print "List length: " + str(len(sub_article)) + "\n"
    for child in sub_article:
        #print child.tag, child.attrib
        for c2 in child:
            print c2.tag, c2.attrib

def get_all_files():
    """
    Return a list of all XML files
    """
    # Testing, return a few, not all
    all_files = []
    all_files.append("lib/elife-articles/elife00003.xml")
    all_files.append("lib/elife-articles/elife00534.xml")
    all_files.append("lib/elife-articles/elife00768.xml")
    all_files.append("lib/elife-articles/elife00778.xml")
    all_files.append("lib/elife-articles/elife00808.xml")
    all_files.append("lib/elife-articles/elife01273.xml")
    all_files.append("lib/elife-articles/elife01893.xml")
    return all_files

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-f", "--file",
                      default="lib/elife-articles/elife00003.xml",
                      action="store", type="string", dest="file",
                      help="Specify the XML file to parse")
    parser.add_option("-a", "--all",
                      default=None,
                      action="store_true", dest="all",
                      help="Parse all files")
    (options, args) = parser.parse_args()
    if options.all:
        xml_files = get_all_files()
    elif options.file:
        xml_files = []
        xml_files.append(options.file)

    for f in xml_files:
        xml_tree = parse_tree(f)
        xml_root = tree_root(xml_tree)

        debug_print(xml_root)
