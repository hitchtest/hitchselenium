from PIL import Image
from functools import reduce
import operator
import math


def similar_images(image1_filepath, image2_filepath, allowable_difference):
    """
    Compare histograms of two images.
    """
    h1 = Image.open(image1_filepath).histogram()
    h2 = Image.open(image2_filepath).histogram()

    rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b)**2, h1, h2)) / len(h1))
    print(rms)
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
    from lxml.html import fromstring
    page_source = fromstring(page_source)
    snippet_parsed = fromstring(html_snippet)

    for page_source_tag in page_source.iter():
        for snippet_tag in snippet_parsed.iter():
            found = True
            if not compare_tags(page_source_tag, snippet_tag):
                found = False
        if found:
            return True
    return False
