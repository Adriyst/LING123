# Class for an object that can generate different XML-elements that I will use multiple
# times in the assignment. Elements used a single time will be handled manually further down.
class XMLFactory:
    # Counters for the IDs
    stanza_counter = 0
    token_counter = 0

    # Function that generates the stanza XML-elements
    def generate_stanza(self, tokens):
        # The best solution to store the string locally for incrementation to work properly
        element = f"""<stanza s-id='{self.stanza_counter+1}'>
            {tokens}
        </stanza>
        """
        self.stanza_counter += 1
        return element

    # Function that generates the word token XML-elements
    def generate_token(self, wordform, rhyme):
        self.token_counter += 1
        return f"""<token t-id='{str(self.stanza_counter+1) + "-" + str(self.token_counter)}'>
                {wordform}{rhyme}
            </token>
            """
    # Function that generates wordform XML-elements
    def generate_wordform(self, value):
        return f"""<wordform>
                    {value}
                </wordform>
                """

    # Function that generates rhyme XML-elements.
    def generate_rhyme(self, value):
        return f"""<rhyme>
                    {value}
                </rhyme>"""

# Instantiating an object of my class
xml = XMLFactory()

# The document I will write to
xml_doc = open("shake.xml", "w")

# The DTD-part of the XML
xml_dtd = """<!DOCTYPE poem [
<!ELEMENT poem (stanza+)>
<!ELEMENT stanza (token+)>
<!ATTLIST stanza s-id CDATA #REQUIRED>
<!ELEMENT token (wordform, rhyme)>
<!ATTLIST token t-id CDATA #REQUIRED>
<!ELEMENT wordform (#PCDATA)>
<!ELEMENT rhyme (#PCDATA)>
]>\n
"""

# Adding meta information about the document, adding the DTD
xml_doc.writelines("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n")
xml_doc.writelines(xml_dtd)
xml_doc.writelines("<poem>\n")

# Counter for the loop on line 7*
lines = 0

# A list of the rhyme pattern in the poem
rhyme_list = ['A', 'A', 'B', 'C', 'C', 'B']
# Variable to hold the tokens for each stanza, instantiated here to avoid potential
# nullpointer exceptions
token_list = ""
# Boolean check for when to add a new stanza
stanzas_check = False

# Looping through the poem to retrieve information
for line in open("shake.txt"):
    # splitting the line into word tokens
    word_array = line.split(" ")
    # looping through the word tokens
    for word in word_array:
        # Check for the final word in the poem
        if word == "fly":
            stanzas_check = True
        # Dont want whitespaces
        if word is "\n":
            break
        # There is an '&' in there, which doesn't comply with what I want in the DTD. Away it goes!
        if word == "&":
            word = "and"
        # Generating elements with the information, using modulo to always get the right rhyme pattern
        word_form = xml.generate_wordform(word.strip())
        word_rhyme = xml.generate_rhyme(rhyme_list[lines % 6])
        word_token = xml.generate_token(word_form, word_rhyme)
        # adding the token to the string that will be used to form the stanza
        token_list += word_token
    # When I hit a new line I know that I am at the end of a stanza
    if line is "\n":
        stanzas_check = True
        # For modulo operations this decremention is necessary
        lines -= 1
    # If we've passed a line shift, generate the stanza XML-element, empty the variable holding
    # the tokens for the current stanza
    if stanzas_check:
        xml_doc.writelines(xml.generate_stanza(token_list))
        token_list = ""
        xml.token_counter = 0
    # Returning the boolean check to false
    stanzas_check = False
    # incrementing
    lines += 1
# Finishing the document
xml_doc.writelines("</poem>")