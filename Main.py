import codecs
import re


##### RETRIEVING ELEMENTS FROM GOT.TXT #####

# Check for when to build the string with the unicorn ascii
unicorn_check = False
# The string that will be built with the unicorn ascii
unicorn_print = ""
# Check for when we're looking at meta information for the title
head_check = False
# The string that will contain the title of the document
doc_title = ""
# The list that will be filled with keywords
keyword_list = []
# The string that will contain the paragraphs
paragraph_list = []

# Looping through the document
for line in open("got.txt"):
    if not unicorn_check:
        # Checking if we're at the top of the document
        if 'doctype' in line:
            unicorn_check = True
    else:
        # Checking if we're at the bottom of the document
        if '<html' not in line:
            # If not we append it to the string
            unicorn_print += line
        else:
            # If we are, we stop looking for more lines for the unicorn
            unicorn_check = False
    if '<head>' in line:
        head_check = True
        # Checking if we're at the correct title-element
    if '<title>' in line and head_check:
        # removing the tags to get the pure text
        doc_title = re.sub(r"<(\W?\w*)>", "", line).strip()
        head_check = False
    # Checking if we're at the correct element containing keywords
    if 'name="keywords"' in line:
        # cleaning up the line to get pure text
        keywords = line.replace('"', '').split('content=')[1].replace(">", "").split(',')
        # adding to new list in case of nullpointer exceptions
        for word in keywords:
            # stripping to get rid of unnecessary whitespace
            keyword_list.append(word.strip())
    # checking if we're at the right paragraphs
    if '<p>' in line or '<p ' in line:
        # removing all the element tags to get the pure text
        line = re.sub(r"<(\W*?\w*?\s*?)*>", "", line).strip()
        paragraph_list.append(line)


##### CREATING NEW HTML DOCUMENT #####

html_start = """<!DOCTYPE html>
"""

html_meta = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
"""

html_middle = """
</head>
<body>
"""

html_end = """
</body>
</html>
"""

# the document title wrapped in the correct elements
doc_title_element = f'<h1><u>{doc_title}</u></h1>'
# the variable to hold the elements for the keywords
keyword_element = "<p>Keywords: "

# looping through list of keywords adding elements
for word_token in keyword_list:
    word_token = f'<em class="keywords">{word_token}</em>, '
    keyword_element += word_token
# cleaning it up to look nicer
keyword_element += "</p>\n"
keyword_element = re.sub(r",\s</p>", "</p>", keyword_element)

# Generating CSS for the keywords
internal_css = """
<style>
    .keywords {
        color: red;
    }
    ul {
        list-style-type: square;
    }
</style>
"""

# wrapping the paragraphs in elements
paragraph_ul = '<ul>'
for para in paragraph_list:
    para = f'<li>{para}</li>\n'
    paragraph_ul += para

paragraph_ul += '</ul>'


##### WRITING TO FILE #####

# html file to write to
html_file = codecs.open('got_clean.html', 'w')
html_file.writelines([html_start, unicorn_print, html_meta, internal_css,
                      html_middle, doc_title_element, "\n", keyword_element,
                      paragraph_ul, html_end])
html_file.close()