import json
import xml.etree.ElementTree as ET

def parse_tree(xml_file):
  return ET.parse(xml_file)
  
def tree_root(tree):
  return tree.getroot()

def parse_root(root):
  """
  Take the root and return sub Elements if found
  """
  front = body = back = sub_article = None

  front = root.find('front')
  body = root.find('body')
  back = root.find('back')
  sub_article = root.findall('sub-article')
  
  return front, body, back, sub_article

def parse_front(root):
  """
  front sub Elements
  """
  
  journal_meta = article_meta = None
  
  journal_meta = root.find('journal-meta')
  article_meta = root.find('article-meta')
  
  return journal_meta, article_meta

def parse_article_meta(root):
  """
  article-meta sub Elements
  TODO: check for when there are single or multiple elements in the DTD
  """
  
  abstract = article_categories = article_id = author_notes = contrib_group = custom_meta_group = elocation_id = funding_group = history = kwd_group = permissions = pub_date = related_article = self_uri = title_group = volume = None
  
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

  return abstract, article_categories, article_id, author_notes, contrib_group, custom_meta_group, elocation_id, funding_group, history, kwd_group, permissions, pub_date, related_article, self_uri, title_group, volume
  
def parse_history(root):
  """
  history sub Elements
  """
  
  date = None
  date = root.find('date')
  return date

def debug_print(root):
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
  
  abstract, article_categories, article_id, author_notes, contrib_group, custom_meta_group, elocation_id, funding_group, history, kwd_group, permissions, pub_date, related_article, self_uri, title_group, volume = parse_article_meta(article_meta)
  
  print "\nChildren of history: "
  print "List length: " + str(len(history)) + "\n"
  for child in history:
    date = parse_history(child)
    print "\nChildren of date: "
    print "List length: " + str(len(date)) + "\n"
    for c2 in date:
      print c2.tag, c2.attrib
  

  # sub-article
  print "\nChildren of sub-article: "
  print "List length: " + str(len(sub_article)) + "\n"
  for child in sub_article:
    #print child.tag, child.attrib
    for c2 in child:
      print c2.tag, c2.attrib
      


if __name__ == '__main__':

  xml_file = 'lib/elife-articles/elife00003.xml'
  tree = parse_tree(xml_file)
  root = tree_root(tree)
  
  debug_print(root)