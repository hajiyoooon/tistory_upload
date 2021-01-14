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

class Node:
    def __init__(self, char):
        self.char = char
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

class MarkdownParser:
    def __init__(self):
        self.root = Node("")
        self.node = self.root

    def parse(self, lines):
        for ch in lines:
            child = Node(ch)
            self.node.add_child(child)
            
            if ch in [HEADER, INDENT]:
                self.node = child

            # elif ch is BLOCK_CODE:
            #     if child.get_parent().get_char() is BLOCK_CODE:
            #         self.node = child.get_parent()
            #     else:
            #         self.node = child

            elif ch is NEW_LINE:
                if child.get_parent().get_char() is BLOCK_CODE:
                    continue
                elif child.get_parent() is not None:
                    self.node = child.get_parent()
            

    def _to_string(self):
        to_string(self.root)

    def _to_html(self):
        to_html(self.root)

def to_html(node):
    childs = node.get_childs()

    for child in childs:
        ch = child.get_char()
        
        if ch in [HEADER, INDENT] :
            print("<h1>",end="")
            to_html(child)
            print("</h1>")
        elif ch is BLOCK_CODE:
            if child.get_parent().get_char() is BLOCK_CODE:
                return 
            else:
                print("<code><pre>")
                to_string(child)
                print("</pre></code>")

        elif ch is NEW_LINE:
            if child.get_parent().get_char() is BLOCK_CODE:
                continue
            else:
                print("</p>")
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


line = " # 안녕하세요\n # 반가워요 \n\n 잘있어요 \n\n > 다시 만나요\n```Java\n int a = 1 \n ```\n # 헤딩"
parser = MarkdownParser()

print("===== parse =====")
parser.parse(line)

print("===== debug =====")
parser._to_html()



