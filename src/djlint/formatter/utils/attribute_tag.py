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
    def __init__(
        self,
        tag: str,
        config: Config,
        attributes: Optional[List] = None,
        properties: Optional[List] = None,
    ):

        self.tag = tag
        self.config = config
        self.raw_attributes = attributes
        self.properties = properties
        self.children = []
        self.data: List[str] = []
        self.name = tag
        self.namespace = None
        self.type: Optional[str] = None

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        self._type = val

    def __get_attribute_name(self, tag: str, attribute: str) -> str:
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
            attribute.lower()
            if attribute.lower() in html_element_attributes["*"]
            or attribute.lower() in html_element_attributes.get(tag, [])
            else attribute
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
        self.output = " ".join(self.data)

        if self.type in [
            "starttag_curly_perc",
            "starttag_comment_curly_perc",
            "starttag_curly_two_hash",
            "starttag_curly_four",
        ]:
            level += 1

        self.output += self.format_contents(level)

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
