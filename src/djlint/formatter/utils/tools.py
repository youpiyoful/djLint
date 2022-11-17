from typing import List


class Softline:
    def __str__(self):
        return "softline"

    def __repr__(self):
        return self.__str__()

    def resolve(self, break_type="hard", indent=""):
        if break_type == "hard":
            return "\n" + indent
        return ""

    def __len__(self):
        return 0


class Line:
    def __str__(self):
        return "line"

    def __repr__(self):
        return self.__str__()

    def resolve(self, break_type="hard", indent="", next=False):
        if break_type == "hard":
            return "\n" + indent
        if next:
            return " "
        return ""

    def __len__(self):
        return 1


class Hardline:
    def __str__(self):
        return "hardline"

    def __repr__(self):
        return self.__str__()

    def resolve(self, indent=""):
        return "\n" + indent

    def __len__(self):
        return 1


def list_builder(elements):
    processed = []
    if isinstance(elements, List):
        for element in elements:
            processed.extend(list_builder(element))

    elif (
        elements
        or isinstance(elements, Softline)
        or isinstance(elements, Hardline)
        or isinstance(elements, Line)
    ):
        processed.append(elements)

    return processed


class Group:
    def __init__(self, elements=[]):
        self.elements = list_builder(elements)

    def appender(self, elements):
        self.elements.extend(list_builder(elements))

    def resolve(self):
        return "".join(self.elements)

    def __str__(self, level=0):
        out = []

        for x, element in enumerate(self.elements):

            if isinstance(element, Indent):
                out.append(element.__repr__(level).strip())
            else:
                out.append(str(element))
        spacing = "\n" + level * "  "
        less_spacing = "\n" + max(level - 1, 0) * "  "
        contents = spacing + (spacing).join(out) + less_spacing
        return f"Group([{contents}])"

    def __repr__(self, level=1):
        spacing = "\n" + level * "  "
        return f"{spacing}{self.__str__(level+1)}\n"

    def __iter__(self):
        for attr in self.elements:
            yield attr

    def __len__(self):
        return sum(len(x) for x in self.elements)

    def __getitem__(self, item):
        return self.elements[item]


class Fill:
    type = "Fill"

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"Fill({self.data})"

    def __repr__(self):
        return "\n  " + self.__str__() + "\n"

    def __len__(self):
        return len(self.__str__())

    def resolve(self, start, end):
        if isinstance(self.data, List):
            data = " ".join(self.data)
        else:
            data = self.data

        allowed_length = end - start
        if len(data) < allowed_length:
            return data

        data = data.split(" ")

        chunk_list = []
        chunk = ""
        for x in data:
            if len(chunk) + len(x) > allowed_length:
                chunk_list.append(chunk)
                chunk = x.lstrip()
            elif chunk != "":
                chunk += " " + x
            else:
                chunk = x.lstrip()
        chunk_list.append(chunk)
        spacing = f"{start * ' '}"
        return spacing + (f"\n{spacing}").join(chunk_list)


class Indent:
    def __init__(self):
        self.elements = []

    def __str__(self, level=0):
        out = []

        for x, element in enumerate(self.elements):

            if isinstance(element, Indent):
                out.append(element.__repr__(level).strip())
            elif isinstance(element, Group):
                out.append(element.__repr__(level).strip())
            else:
                out.append(str(element))
        spacing = "\n" + level * "  "
        less_spacing = "\n" + max(level - 1, 0) * "  "
        contents = spacing + (spacing).join(out) + less_spacing
        return f"Indent([{contents}])"

    def __repr__(self, level=1):
        spacing = "\n" + level * "  "
        return f"{spacing}{self.__str__(level+1)}\n"

    def appender(self, element):
        self.elements.extend(list_builder(element))

    def get_elements(self):
        return self.elements

    def __len__(self):
        return sum(len(x) for x in self.elements)


ROOT_TAG_NAME = "djlint"
DATA_TAG_NAME = "djlint-data"

VOID = "void"
CLOSE = "close"
DOCTYPE = "doctype"
ENDTAG_CURLY_PERC = "endtag_curly_perc"
ENDTAG_CURLY_TWO_SLASH = "endtag_curly_two_slash"
ENDTAG_CURLY_FOUR_SLASH = "endtag_curly_four_slash"
ENDTAG_COMMENT_CURLY_PERC = "endtag_comment_curly_perc"
OPEN = "open"
STARTTAG_CURLY_PERC = "starttag_curly_perc"
STARTTAG_CURLY_FOUR = "starttag_curly_four"
STARTTAG_CURLY_TWO_HASH = "starttag_curly_two_hash"
STARTTAG_COMMENT_CURLY_PERC = "starttag_comment_curly_perc"

COMMENT_CURLY_HASH = "comment_curly_hash"
COMMENT_AT_STAR = "comment_at_star"
COMMENT = "comment"

CURLY_TWO_EXCAIM = "curly_two_exlaim"
CURLY_TWO = "curly_two"
SLASH_CURLY_TWO = "slash_curly_two"
CURLY_THREE = "curly_three"

ALL_CLOSE_TYPES = [
    CLOSE,
    ENDTAG_CURLY_PERC,
    ENDTAG_CURLY_TWO_SLASH,
    ENDTAG_CURLY_FOUR_SLASH,
    ENDTAG_COMMENT_CURLY_PERC,
]
ALL_CLOSE_TEMPLATE_TYPES = [
    ENDTAG_CURLY_PERC,
    ENDTAG_CURLY_TWO_SLASH,
    ENDTAG_CURLY_FOUR_SLASH,
    ENDTAG_COMMENT_CURLY_PERC,
]
ALL_OPEN_TYPES = [
    OPEN,
    STARTTAG_CURLY_PERC,
    STARTTAG_CURLY_FOUR,
    STARTTAG_CURLY_TWO_HASH,
    STARTTAG_COMMENT_CURLY_PERC,
]
ALL_OPEN_TEMPLATE_TYPES = [
    STARTTAG_CURLY_PERC,
    STARTTAG_CURLY_FOUR,
    STARTTAG_CURLY_TWO_HASH,
    STARTTAG_COMMENT_CURLY_PERC,
]
ALL_COMMENT_TYPES = [COMMENT, COMMENT_CURLY_HASH, COMMENT_AT_STAR]
ALL_STATEMENT_TYPES = [CURLY_TWO_EXCAIM, CURLY_TWO, SLASH_CURLY_TWO, CURLY_THREE]

HAS_TRAILING_SPACE = "has-trailing-space"
HAS_TRAILING_BREAK = "has-trailing-break"
SPACELESS_LEFT_DASH = "spaceless-left-dash"
SPACELESS_LEFT_TILDE = "spaceless-left-tilde"
SPACELESS_LEFT_PLUS = "spaceless-left-plus"
SAFE_LEFT = "safe-left"
PARTIAL = "partial"
SPACELESS_RIGHT_DASH = "spaceless-right-dash"
SPACELESS_RIGHT_TILDE = "spaceless-right-tilde"
SPACELESS_RIGHT_PLUS = "spaceless-right-plus"
