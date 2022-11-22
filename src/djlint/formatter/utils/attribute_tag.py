"""Attribute tag additions to the base Tag class.

The only purpose of this class is to keep logic that is
dedicated to the attributes separated from the standard
Tag logic.

Also formatting of attribute is done slightly differently than
the html tag formatting.
"""
import re
from typing import Dict, List, Optional, Tuple, Union

from HtmlElementAttributes import html_element_attributes

from djlint.settings import Config

from .tools import Fill, Group, Hardline, Indent, Line, Softline, list_builder


class AttributeTag:
    # any override methods here.
    ROOT_TAG_NAME = "djlint-attribute"
    SINGLE_QUOTE = "djlint-single-quote"
    DOUBLE_QUOTE = "djlint-double-quote"

    def __init__(
        self,
        tag: str,
        config: Config,
        parent_tag: str,
        indent_padding: int = 0,
        attributes: Optional[List] = None,
        properties: Optional[List] = None,
    ):

        self.tag = tag
        self.config = config
        self.parent = None
        self.parent_tag = parent_tag
        self.previous_tag = None
        self.next_tag = None
        self.raw_attributes = attributes
        self.properties = properties or []
        self.children = []
        self.data: List[str] = []
        self.base_level = 0
        self.indent_padding = indent_padding
        self.output = []
        self.has_quoted_value = False

        self.namespace = None
        self.type: Optional[str] = None

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        self._type = val

    @property
    def name(self):
        if self.data:
            return self.data[0]
        return self.tag

    def _previous_with_prop(self, prop):

        if self.previous_tag:
            if prop in self.previous_tag.properties:
                return self.previous_tag

            return self.previous_tag._previous_with_prop(prop)
        return None

    def _next_with_prop(self, prop):

        if self.next_tag:
            if prop in self.next_tag.properties:
                return self.next_tag

            return self.next_tag._next_with_prop(prop)
        return None

    def _nested_quote_level(self, level=0):

        if self.parent:
            if self.parent.type in [self.DOUBLE_QUOTE, self.SINGLE_QUOTE]:
                level += 1

            level += self.parent._nested_quote_level(level)

        return level

    @property
    def _get_quote(self):
        # check the nested level of the quote.

        if self.type not in [self.DOUBLE_QUOTE, self.SINGLE_QUOTE]:
            return ""

        level = self._nested_quote_level()

        if level == 0:
            return '"'
        elif level == 1:
            return "'"
        elif level % 2 == 0:
            return '"'
        return "'"

    @property
    def _has_leading_space(self) -> bool:
        if self.previous_tag and self.previous_tag._has_trailing_space:
            return True

        # or if we are the first child of a parent w/ trailing space
        if (
            self.parent
            and self.parent._has_trailing_space
            and self.parent.children[0] == self
        ):
            return True

    @property
    def _has_trailing_space(self) -> bool:
        return "has-trailing-space" in self.properties

    @property
    def _has_value(self) -> bool:
        return "has-value" in self.properties

    @property
    def _break_before(self) -> bool:
        if (
            "has-trailing-space" in self.previous_tag.properties
        ):  # and self._is_in_attribute_value is False:
            return ""  # return "\n"

        return ""

    @property
    def _break_after(self) -> str:
        if self.name == self.ROOT_TAG_NAME and self.children:
            return Softline()

    @property
    def _space_before(self) -> str:

        if (
            self.parent
            and self.parent.name == self.ROOT_TAG_NAME
            and not self.previous_tag
        ):
            return Line()

        if self._has_leading_space:

            if self.previous_tag and self.previous_tag._has_trailing_space:
                return ""
            if (
                self.parent
                and self.parent.name in [self.SINGLE_QUOTE, self.DOUBLE_QUOTE]
                and self.parent.previous_tag
                and not self.parent.previous_tag._has_value
            ):
                return " "

    def last_child(self):
        if self.children:
            return self.children[-1]

        return None

    @property
    def _space_after(self) -> str:

        if (
            not self.next_tag
            and self.tag != self.ROOT_TAG_NAME
            and self.parent
            and self.parent.name not in [self.SINGLE_QUOTE, self.DOUBLE_QUOTE]
        ):
            return Softline()

        if self._has_trailing_space:
            if (
                self.parent
                and self.parent.name in [self.SINGLE_QUOTE, self.DOUBLE_QUOTE]
                and self.parent.previous_tag
                and not self.parent.previous_tag._has_value
            ):
                # if (re.search(r"\s$", self._get_raw_data(), re.M)
                #     or self.next_tag  and re.search(r"^\s", self.next_tag._get_raw_data(), re.M)):
                #     return ""
                return " "

            if self.name[-1] in ["{", ":", ","]:
                """
                Keep nice formatting on spread out attributes.

                attrib="{ this: true, that:false }"
                         ^     ^     ^
                """
                return " "

            if self.next_tag and self.next_tag.name[0] in ["}"]:
                """
                Keep nice formatting on spread out attributes.

                attrib="{ this: true }"
                                    ^
                """
                return " "

            if self._nested_quote_level() < 1:
                return Line()

        if (
            self.name in [self.SINGLE_QUOTE, self.DOUBLE_QUOTE]
            and self.last_child()
            and not self.last_child().next_tag
        ):
            # if the last item
            return ""

        if self.name in [self.SINGLE_QUOTE, self.DOUBLE_QUOTE]:
            if self._nested_quote_level() < 1:
                return Line()

        return ""

    def __get_attribute_name(self, tag) -> str:
        """
        Returns lowerized attribute name if it is a knowed attribute from
        function ``HtmlElementAttributes.html_element_attributes``.

        Arguments:
            tag (string): The HTML element name.
            attribute (string): The attribute name.

        Returns:
            string: Attribute name.
        """
        return (
            tag.lower()
            if tag.lower() in html_element_attributes["*"]
            or tag.lower() in html_element_attributes.get(self.parent_tag, [])
            else tag
        )

    def _get_raw_data(self):
        if self.data:
            return " ".join(self.data)
        return ""

    def format_contents(self, level=0):
        """
        Return formatted output of current element children.

        Arguments:
            level (integer): Current element level in HTML tree.

        Returns:
            string: A string including a recursive output of children.
        """
        s = []
        for child in self.children:
            formated = child.format()
            s.extend(list_builder(formated))

        return s

    def appender(self, stuff):
        self.output.extend(list_builder(stuff))

    def format(self, level=0):

        # print(self.name, self.properties)
        self.appender(self._space_before)

        self.appender(" ".join([self.__get_attribute_name(x) for x in self.data]))

        quote = self._get_quote

        if self._has_value:
            self.appender("=")

        self.appender(quote)

        if self.tag in [self.SINGLE_QUOTE, self.DOUBLE_QUOTE]:
            contents = Group()
        else:
            contents = Indent()
        contents.appender(self.format_contents())

        self.appender(contents)
        self.appender(quote)
        self.appender(self._space_after)

        self.appender(self._break_after)

        return self.output

    @property
    def statement_tag(self):
        return self.tag
