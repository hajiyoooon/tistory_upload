import re

HEADER = "#"
INDENT = ">"

NEW_LINE = "\n"
TAB = "\t"

ORDERED_LIST_ONE = "1."
ORDERED_LIST_TWO = "2."
ORDERED_LIST_THREE = "3."

UNORDERED_LIST_DASH = "-"
UNORDERED_LIST_STAR = "*"
UNORDERED_LIST_PLUS = "+"

BLOCK_CODE = "```"
INLINE_CODE ="`"

TITLE_REGEX = re.compile("^[#].* ")
INLINE_LINK_REGEX = re.compile("\[[가-힣A-Za-z].*\]\(.*\)")
HREF_REGEX = re.compile("http:\/\/[가-힣A-Za-z].*[A-Za-z]")
LINK_INFO_REGEX = re.compile("\[[가-힣A-Za-z].\]")
ITALIC_REGEX = re.compile("\*.*\*")
BOLD_REGEX = re.compile("\*\*.*\*\*")
INLINE_CODE_REGEX = re.compile("\`.*\`")
HIGHLIGHT_REGEX = re.compile("==.*==")
IMAGE_REGEX = re.compile("!\[.*\]\(.*\)")
IMAGE_INFO_REGEX = re.compile("\[.*\]")
IMAGE_URI_REGEX = re.compile("\(.*\)")

types = ['heading', 'character', 'image', 'blockquote', 'code_block', 'code_inline', 'nonetype']

class Node:
    def __init__(self, char):
        self.char = char
        self.type = 'nonetype'

        self.parent = None
        self.childs = list()

    def set_parent(self, node):
        self.parent = node

    def get_parent(self):
        return self.parent

    def add_child(self, child):
        child.set_parent(self)
        self.childs.append(child)

    def has_child(self):
        return len(self.childs) != 0

    def get_childs(self):
        return self.childs

    def get_char(self):
        return self.char

    def set_type(self, type):
        self.type = type

class MarkdownParser:
    def __init__(self):
        self.root = Node("p")
        self.node = self.root

    idx = 0
    def parse(self, lines):
        line = lines[0]
        idx = 0
        while True:
            g = TITLE_REGEX.search(line.lstrip())
            if type(g) != type(None):
                self.node.set_type('heading')
                line = re.sub(TITLE_REGEX, line)
                child = Node(line)
                self.node.add_child(child)
                continue

            else:
                idx += 1
                line = lines[idx]

    def _to_string(self):
        to_string(self.root)

    def _to_html(self):
        to_html(self.root)

def to_html(node):
    childs = node.get_childs()

    for child in childs:
        ch = child.get_char()
        
        if ch is HEADER:
            print("<h1>",end="")
            to_html(child)
            print("</h1>")

        elif ch is INDENT:
            print("<blockquote>",end="")
            to_html(child)
            print("</blockquote>")
        # elif ch is BLOCK_CODE:
        #     if child.get_parent().get_char() is BLOCK_CODE:
        #         return 
        #     else:
        #         # print("<code><pre>")
        #         to_string(child)
        #         # print("</pre></code>")

        elif ch is NEW_LINE:
            print("</p>", end="")
            return
        else:
            print(ch, end="")
            
def to_string(node):
    childs = node.get_childs()

    for child in childs:
        print(child.get_char(), end="")
        if child.get_char is NEW_LINE :
            print()

        if(child.has_child()):
            to_string(child)


line = " # 안녕하세요\n # 감사해요\n > 이건 블록 주석 \n >> 블록주석2 \n"
parser = MarkdownParser()

print("===== parse =====")
parser.parse(line)

print("===== debug =====")
parser._to_html()
print()

# print("===== debug =====")
# parser._to_string()



