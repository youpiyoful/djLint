"""Attribute tag additions to the base Tag class.

The only purpose of this class is to keep logic that is
dedicated to the attributes separated from the standard
Tag logic.

Also formatting of attribute is done slightly differently than
the html tag formatting.
"""
from typing import Dict, List, Optional, Tuple, Union

from HtmlElementAttributes import html_element_attributes

from djlint.settings import Config


class AttributeTag:
    # any override methods here.
    ROOT_TAG_NAME = "djlint-attribute"
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

    @property
    def _attribute_value_start(self):
        if "has-value" in self.properties:
            if 'has-value-start-double' in self.properties:
                return "has-value-start-double"
            if 'has-value-start-single' in self.properties:
                return 'has-value-start-single'

        return False

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

    @property
    def _is_in_attribute_value(self) -> bool:
        # search for the previous attribute open
        if self.previous_tag:
            attribute_value_start = self.previous_tag._attribute_value_start

            if attribute_value_start:
                # found a start tag, now make sure it was not closed.
                # print(attribute_value_start, self._previous_with_prop(attribute_value_start).name, self._previous_with_prop(attribute_value_start).properties)
                previous = self._previous_with_prop(attribute_value_start)
                previous_props = previous.properties if previous else []

                next = self._next_with_prop(attribute_value_start)
                next_props = next.properties if next else []
                # if previous and next:
                #     print(self.name, previous.name, next.name)
                if "has-value" in previous_props and "has-value" not in next_props:
                    return True
            return self.previous_tag._is_in_attribute_value

        return False

    @property
    def _is_nested_attribute_value(self) -> bool:
        if self._is_in_attribute_value is False:
            return False

        if self._has_trailing_quote:
            # if myself has a closing quote, use it.
            return False

        if self.next_tag:
            if ('has-value-start-single' in self.next_tag.properties or 'has-value-start-double' in self.next_tag.properties):
                return True
            return self.next_tag._is_nested_attribute_value
        return False

    @property
    def _has_trailing_quote(self) -> bool:
        return (('has-value-start-double' in self.properties
            or 'has-value-start-single' in self.properties
            ) and 'has-value' not in self.properties)

    @property
    def _break_before(self) -> bool:
        if "has-trailing-space" in self.previous_tag.properties and self._is_in_attribute_value is False:
            return "\n"

        return ""

    @property
    def _break_after(self) -> str:
        if "has-trailing-space" in self.properties and (self._is_in_attribute_value is False or self._has_trailing_quote):

            return "\n" + self.indent_padding * " " + " "

        if "has-trailing-space" in self.properties and self.next_tag and not self._has_trailing_quote and not self._is_nested_attribute_value:
            return " "

        return ""

    @property
    def _space_after(self) -> str:
        # print(self.name)
        if "has-trailing-space" in self.properties and self._is_nested_attribute_value:
            return " "

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

    def format_contents(self, level):
        """
        Return formatted output of current element children.

        Arguments:
            level (integer): Current element level in HTML tree.

        Returns:
            string: A string including a recursive output of children.
        """
        s = []
        for child in self.children:

            s.append(child.format(level))

        return "".join(s)


    def format(self, level=0):

        self.output = ''
        if self.name == self.ROOT_TAG_NAME and self.children:
            self.output += " "
        # print(self.type, self.name,self.properties)
        # print(self.data, self.properties, self.parent_tag, len(self.children), (self.children[0].data if self.children else ""))
        # if len(self.data) > 1:
        #     raise ValueError("data is too long:", self.data)

        self.output += " ".join([self.__get_attribute_name(x) for x in self.data])

        quote = "'" if self._is_nested_attribute_value else '"'

        if "has-value" in self.properties:
            self.output += "="
            # if "has-value-start" in self.properties:
            self.output += quote

        if self.type in [
            "starttag_curly_perc",
            "starttag_comment_curly_perc",
            "starttag_curly_two_hash",
            "starttag_curly_four",
        ]:
            level += 1

        self.output += self.format_contents(level)

        self.output += self._space_after

        if self._has_trailing_quote:
            self.output += quote

        self.output += self._break_after

        if self.type in [
            "endtag_curly_perc",
            "endtag_comment_curly_perc",
            "endtag_curly_two_slash",
            "endtag_curly_four_slash",
        ]:
            level -= 1

        return self.output

    @property
    def statement_tag(self):
        return self.tag
