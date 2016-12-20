from PIL import Image
from functools import reduce
import operator
import math


def similar_images(image1_filepath, image2_filepath, allowable_difference):
    """
    Compare histograms of two images.
    """
    hist1 = Image.open(image1_filepath).histogram()
    hist2 = Image.open(image2_filepath).histogram()

    rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b)**2, hist1, hist2)) / len(hist1))
    return rms < allowable_difference


def compare_tags(tag1, tag2):
    """
    Compare equivalent tags.

    According to HTML specification <tag a="1" b="2" c="3">contents</tag>
    is equivalent to <tag b="2" c="3" a="1">contents</tag>
    """
    return tag1.tag == tag2.tag and tag1.text == tag2.text and tag1.attrib == tag2.attrib


def check_page_contains_html(page_source, html_snippet):
    """
    Check that parsed HTML text contains a parsed snippet of HTML.
    """
    from lxml.html import fragments_fromstring, fromstring, tostring
    page_source_tags = [x for x in fromstring(page_source).iter()]
    snippet_parsed_tags = [x for x in fragments_fromstring(html_snippet)]

    for index, tag in enumerate(page_source_tags):
        if compare_tags(tag, snippet_parsed_tags[0]):
            matching = True
            for index2, potentially_matching_tag in enumerate(page_source_tags[index:index + len(snippet_parsed_tags)]):
                potentially_subsequent_matching_tag = snippet_parsed_tags[index2]
                if not compare_tags(potentially_subsequent_matching_tag, potentially_matching_tag):
                    matching = False
            return matching
    return False
