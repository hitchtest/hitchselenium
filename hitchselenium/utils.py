from PIL import Image
from functools import reduce
import operator
import math


def image_similarity_score(image1_filepath, image2_filepath):
    """
    Compare histograms of two images.
    """
    hist1 = Image.open(image1_filepath).histogram()
    hist2 = Image.open(image2_filepath).histogram()
    return math.sqrt(reduce(operator.add, map(lambda a, b: (a - b)**2, hist1, hist2)) / len(hist1))


#def compare_text(name1, name2, simex):
    #if name1 is None or name2 is None:
        #return name1 is None and name2 is None
    #else:
        #return simex.compile(name2).match(name1) is not None


#def compare_tags(tag1, tag2, simex):
    #"""
    #Compare equivalent tags.

    #According to HTML specification <tag a="1" b="2" c="3">contents</tag>
    #is equivalent to <tag b="2" c="3" a="1">contents</tag>
    #"""
    #return compare_text(tag1.tag, tag2.tag, simex) and \
        #compare_text(tag1.text, tag2.text, simex) and \
        #compare_text(tag1.tail, tag2.tail, simex) and \
        #tag1.attrib == tag2.attrib


#def check_page_contains_html(page_source, html_snippet, simex):
    #"""
    #Check that parsed HTML text contains a parsed snippet of HTML.
    #"""
    #from lxml.html import fragments_fromstring, fromstring, tostring
    #from itertools import chain
    #page_source_tags = [x for x in fromstring(page_source).iter()]
    #snippet_parsed_tags = list(chain(*[[tag for tag in frag.iter()] for frag in fragments_fromstring(html_snippet)]))

    #for index, tag in enumerate(page_source_tags):
        #if compare_tags(tag, snippet_parsed_tags[0], simex):
            #matching = True
            #for index2, potentially_matching_tag in enumerate(page_source_tags[index:index + len(snippet_parsed_tags)]):
                #potentially_subsequent_matching_tag = snippet_parsed_tags[index2]
                #if not compare_tags(potentially_subsequent_matching_tag, potentially_matching_tag, simex):
                    #matching = False
            #return matching
    #return False
