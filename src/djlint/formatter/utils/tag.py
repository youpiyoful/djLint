"""Base tag class.

A tag represents any html/template element.
"""

import re
from itertools import chain
from typing import Dict, List, Optional, Tuple, Union

from HtmlStyles import html_styles
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements

from djlint.settings import Config

from .attribute_builder import AttributeTreeBuilder


class Tag:
    """
    The base node of a HTML tree.

    Arguments:
        tag (string): The HTML element name, like ``div``, ``a``, ``caption``, etc..
        config (djlint.settings.Conf): The parser config object.

    Keyword Arguments:
        parent (Tag): A tag object of this element parent if any.
        attributes (str): string of potential attributes for an html element or
            template tag.
        properties (list): Some 'virtual' properties specific to some tags that may
            define special behaviors.
    """

    ROOT_TAG_NAME = "djlint"
    DATA_TAG_NAME = "djlint-data"

    def __init__(
        self,
        tag: str,
        config: Config,
        parent: Optional["Tag"] = None,
        attributes: Optional[str] = None,
        properties: Optional[List] = [],
    ) -> None:

        self.__css_default_whitespace = "normal"
        self.__css_default_display = "inline"
        self.__css_whitespace = self.__get_tag_style("white-space")

        self.__css_display = dict(
            list(self.__get_tag_style("display").items())
            + list(
                {
                    "button": "inline-block",
                    "template": "inline",
                    "source": "block",
                    "track": "block",
                    "script": "block",
                    "param": "block",
                    "details": "block",
                    "summary": "block",
                    "dialog": "block",
                    "meter": "inline-block",
                    "progress": "inline-block",
                    "object": "inline-block",
                    "video": "inline-block",
                    "audio": "inline-block",
                    "select": "inline-block",
                    "option": "block",
                    "optgroup": "block",
                }.items()
            ),
        )
        self.data: List[str] = []
        self.type: Optional[str] = None
        self._is_html = False
        self.parent = parent
        self.config = config
        self.previous_tag = None
        self.next_tag = None
        self.rawname = tag
        self.children = []
        self.output = []
        self.hidden = False
        self.tag = tag
        self.namespace, self.name = self.__get_tag_name()
        self.is_pre = self.__tag_is_pre(self.name)
        self.raw_attributes = attributes
        self.raw_properties = properties or []
        self.is_void = self.name in html_void_elements + ["extends", "load", "include"]
        self.indent_padding = 0

    def __str__(self) -> str:
        return self.name

    @property
    def data(self) -> Optional[str]:
        return self._data

    @data.setter
    def data(self, val: str) -> None:
        self._data = val

    @property
    def type(self) -> Optional[str]:
        return self._type

    @type.setter
    def type(self, val: str) -> None:
        self._type = val

    @property
    def is_html(self) -> Optional[str]:
        """
        Describe if Tag is an HTML element (as defined from Tag argument).

        This is more of a shortand since this method does not make any assertion and
        only returns what have been set in ``Tag._is_html`` instance attribute. On
        default, a Tag is not assumed as an HTML element, you need to set it yourself
        on the instance attribute.

        TODO: Despite return is typed to string, you may be able to just set instance
        attribute to ``True`` to qualify element as HTML.

        Returns:
            string: The value of ``Tag._is_html`` instance attribute. It may be
            ``False`` if attribute has never be explicitely set.
        """
        return self._is_html

    @is_html.setter
    def is_html(self, val: str) -> None:
        """
        Setter method to define value of ``Tag._is_html`` attribute.

        TODO: Despite typed as a string, the practical usage of is_html is boolean so
        it should be safe enough to type it as a boolean.

        Arguments:
            val (string): Value to set.
        """
        self._is_html = val


    def first_child(self):
        if self.children:
            return self.children[0]

        return None

    def last_child(self):
        if self.children:
            return self.children[-1]

        return None


    def set_profile(self, profile) -> str:
        # todo: add config setting to disable profile guessing
        if self.config.profile == "all":
            self.config.profile = profile

        # set all parents
        if self.parent:
            self.parent.set_profile(profile)

    def get_profile(self) -> str:
        if self.config.profile != "all":
            return self.config.profile

        if self.parent:
            return self.parent.get_profile()

        return self.config.profile

    def __get_template_space(self) -> str:
        """
        Returns a possible whitespace character that will be include inside the
        template tag on the left and right position of the tag.

        Returns:
            string: A single whitespace if the profile is not handlebars.
            else return an empty string.
        """
        # if profile == handlebars or mustache, exclude the spaces.
        # we should try to guess the profile......

        return " " if self.get_profile() != "handlebars" else ""

    def __get_partial(self) -> str:
        """
        Returns possible character to describe a partial marker at left position
        inside an element tag.

        This is only for the curly tag syntax which support it like Handlebars.

        Returns:
            string: A single right caret if element has the property ``partial``
            else return an empty string.
        """

        return "> " if "partial" in self.raw_properties else ""

    def __get_safe_left(self) -> str:
        if "safe-left" in self.raw_properties:
            return "--"

        return ""

    def __get_spaceless_left(self) -> str:
        """
        Returns possible character to describe a spaceless marker at left position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.

        Returns:
            string: A single hyphen if element have the property ``spaceless-left``
            else return an empty string.
        """
        if "spaceless-left-dash" in self.raw_properties:
            return "-"

        if "spaceless-left-tilde" in self.raw_properties:
            return "~"

        if "spaceless-left-plus" in self.raw_properties:
            return "+"

        return ""

    def __get_spaceless_right(self) -> str:
        """
        Returns possible character to describe a spaceless marker at right position
        inside an element tag.

        This is only for the curly tag syntax which support it like Jinja.

        Returns:
            string: A single hyphen if element have the property ``spaceless-right``
            else return an empty string.
        """
        if "spaceless-right-dash" in self.raw_properties:
            return "-"

        if "spaceless-right-tilde" in self.raw_properties:
            return "~"

        if "spaceless-right-plus" in self.raw_properties:
            return "+"

        return ""

    def __get_tag_closing(self) -> str:
        """
        Returns element HTML tag ending syntax.

        Returns:
            string: `` />`` if element is a void HTML element, else ``>``.
        """
        if self.is_void:
            return " />"

        if self._is_html:
            if self.type == "comment":
                return "-->"
            return ">"

        if self.type in ["starttag_curly_perc", "endtag_curly_perc"]:
            return self.__get_spaceless_right() + "%}"

        if self.type in ["starttag_curly_four", "endtag_curly_four_slash"]:
            return self.__get_spaceless_right() + "}}}}"

        if self.type in [
            "curly_two_exlaim",
            "curly_two",
            "starttag_curly_two_hash",
            "endtag_curly_two_slash",
            "slash_curly_two",
        ]:
            return self.__get_spaceless_right() + "}}"

        if self.type == "curly_three":
            return self.__get_spaceless_right() + "}}}"
        if self.type == "comment_curly_hash":
            return self.__get_spaceless_right() + "#}"
        return ""

    def __get_tag_opening(self):
        if self.type in ["starttag_curly_perc", "endtag_curly_perc"]:
            return "{%" + self.__get_spaceless_left()

        if self.type == "starttag_curly_four":
            return "{{{{" + self.__get_spaceless_left()

        if self.type == "curly_three":
            return "{{{" + self.__get_spaceless_left()

        if self.type == "starttag_curly_two_hash":
            return f"{{{{{self.__get_spaceless_left()}#"

        if self.type == "endtag_curly_four_slash":
            return f"{{{{{{{{{self.__get_spaceless_left()}/"

        if self.type == "endtag_curly_two_slash":
            return f"{{{{{self.__get_spaceless_left()}/"

        if self.type == "curly_two":
            return "{{" + self.__get_spaceless_left()

        if self.type == "curly_two_exlaim":
            return "{{!" + self.__get_spaceless_left()

        if self.type == "comment" and self.is_html:
            return "<!--"

        if self.type == "slash_curly_two":
            return "\\{{" + self.__get_spaceless_left()

        if self.type == "comment_curly_hash":
            return "{#" + self.__get_spaceless_left()


        if self.name.lower() == "doctype":
            return "<!"

        return "<"

    def __get_tag_modifier(self):
        if self.type == "endtag_curly_perc":
            return "end"
        return ""

    @property
    def open_tag(self) -> str:
        """
        Returns element HTML opening tag including its possible attributes.

        * If element is a HTML element, this will be the HTML opening tag like
          ``<p>``;
        * If element is a curly element with percent, this will be its closing form like
          ``{% endtag %}``;
        * Finally if element is not a HTML or a curly element, this will be an empty
          string.

        Returns:
            string: Opening tag string if available.
        """
        if self._is_html:

            start = f"{self.__get_tag_opening()}{self.name}"
            self.indent_padding = len(start)

            if self.parent and (
                self.parent.is_indentation_sensitive or self.parent.is_whitespace_sensitive
            ):

                return f"{start}{self._attributes}{self.__get_tag_closing()}"
            else:
                return f"{start}{self._attributes}{self.__get_tag_closing()}"

        start = f"{self.__get_tag_opening()}{self.__get_partial()}{self.__get_template_space()}{self.tag}"

        self.indent_padding = len(start)

        return (
            f"{start}{self._attributes}{self.__get_template_space()}{self.__get_tag_closing()}"

        )

    @property
    def close_tag(self) -> str:
        """
        Returns element HTML closing tag.

        * If element is a HTML element and not a void HTML element, this will
          be the HTML closing tag like ``</p>``;
        * If element is a curly element with percent, this will be its closing form like
          ``{% endtag %}``;
        * Finally if element is not a HTML or a curly element, this will be an empty
          string.

        Returns:
            string: Closing tag string if available.
        """

        if self.is_void or self.type in ["comment"]:
            return ""

        if self._is_html:
            if self.parent and (
                self.parent.is_indentation_sensitive or self.parent.is_whitespace_sensitive
            ):
                return f"</{self.name}{self.__get_tag_closing()}"
            return f"</{self.name}{self.__get_tag_closing()}"

        if self.type in [
            "endtag_curly_perc",
            "endtag_curly_two_slash",
            "endtag_curly_four_slash",
            "endtag_comment_curly_perc",
        ]:

            return (
                f"{self.__get_tag_opening()}{self.__get_partial()}{self.__get_safe_left()}{self.__get_template_space()}{self.__get_tag_modifier()}{self.tag}{self._attributes}{self.__get_template_space()}"
                f"{self.__get_tag_closing()}"
            )
        return ""

    @property
    def statement_tag(self) -> str:
        """
        Returns element statement tag.

        Returns:
            string: The statement tag or an empty string, depending if element is a
            curly element or not.
        """
        return f"{self.__get_tag_opening()}{self.__get_partial()}{self.__get_safe_left()}{self.__get_template_space()}{self.tag}{self._attributes}{self.__get_template_space()}{self.__get_tag_closing()}"

    def __get_tag_style(self, style: str) -> Dict:
        """
        Returns all HTML element default value for given CSS property as defined from
        HTML5 W3C specification.

        Arguments:
            style (string): CSS property name to search for.

        Returns:
            dict: A dictionnary of all HTML element which have a default value for
            given CSS property. Where item key is the element name and item value is
            the default property value.
        """
        return dict(
            chain(
                *map(
                    dict.items,
                    [
                        {
                            y.strip(): x["style"].get(style)
                            for y in x["selectorText"].split(",")
                        }
                        for x in list(
                            filter(
                                lambda x: x["style"].get(style) is not None,
                                html_styles,
                            )
                        )
                    ],
                )
            )
        )

    def __tag_is_pre(self, tag: str) -> bool:
        """
        Describe if Tag have preformatted text behavior.

        Element preformatted text status is determined from default element styles
        according to W3C CSS specifications.

        Whatever status is, if ``Tag._is_html`` is ``False`` this will always return
        ``False``.

        Returns:
            bool: True if element have a preformatted text behavior else ``False``.
        """
        if self._is_html:
            return self.__css_whitespace.get(
                tag, self.__css_default_whitespace
            ).startswith("pre")
        return False

    @property

    def is_whitespace_sensitive(self) -> bool:
        """
        Check if tag is space sensitive.

        Space sensitivity is based on element CSS flow. If element is HTML, have a
        block alike flow and not a script element, it is not considered as sensitive.

        Returns:
            bool: A boolean whether the element is space sensitive or not.
        """

        # if self._is_html:
        #     display = self.__css_display.get(self.name, self.__css_default_display)

        return (
            self.is_script
            #or not display.startswith("table")
            #and display not in ["block", "list-item", "inline-block"]
            or self.is_indentation_sensitive
        )

        # return False

    @property
    def is_front_matter(self) -> bool:
        return False

    @property
    def is_first_child_leading_space_sensitive_css_display(self) -> bool:
        return False

    @property
    def is_next_leading_space_sensitive_css_display(self) -> bool:
        return False

    @property
    def is_leading_space_sensitive(self) -> bool:
        """
        Check if tag is sensitive to leading space.
        """

        if self.is_front_matter:
            return False

        if self.type == self.DATA_TAG_NAME:
            return True

        if self.is_pre:
            return True

        if not self.previous_tag and (self.parent.type == self.ROOT_TAG_NAME or self.is_script or not self.parent.is_first_child_leading_space_sensitive_css_display):
            return False

        if self.previous_tag and not self.previous_tag.is_next_leading_space_sensitive_css_display:
            return False

        return True

    @property
    def is_indentation_sensitive(self) -> bool:
        """
        Check if tag is indentation sensitive.

        Indentation sensitivity is based on element CSS flow. If element is HTML and
        have a 'pre' alike flow it is considered as sensitive.

        TODO: It seems '__tag_is_pre' have already been used in 'self.is_pre' from
        '__init__' so it should be safe to rely on this instance attribute instead of
        running '__tag_is_pre' again each time 'is_indentation_sensitive' is called.

        Returns:
            bool: A boolean whether the element is indentation sensitive or not.
        """
        if self._is_html:
            return self.__tag_is_pre(self.name)

        return False


    @property
    def is_dangling_space_sensitive(self) -> bool:
        return not self.is_script and self.__css_display.get(self.name, self.__css_default_display) !="inline-block" and not self.is_display_block_like


    @property
    def is_display_none(self) -> bool:
        """
        Describe if Tag is an hidden element.

        Element hidden status is determined from element CSS flow (block,
        inline, table, etc..) as defined in HTML specifications, element CSS style rules
        is not involved here.

        Whatever hidden status is, if ``Tag._is_html`` is ``False`` this will always
        return ``False``.

        TODO: This property is a little disturbing with the ``Tag.hidden`` attribute
        that does not seem to fullfill the same purpose.

        Returns:
            bool: True if element have a hidden status like body, meta, etc.. else
            ``False``.
        """
        if self._is_html:
            return (
                self.__css_display.get(self.name, self.__css_default_display) == "none"
            )

        return False

    @property
    def is_display_block_like(self) -> bool:
        display =  self.__css_display.get(self.name, self.__css_default_display)
        return (
               display in ['block', 'list-item'] or display.startswith('table')
            )
    @property
    def has_trailing_space(self) -> bool:
        return 'has-trailing-space' in self.raw_properties
    @property
    def is_last_child_trailing_space_sensitive_css_display(self) ->bool:
        return False

    @property
    def is_prev_trailing_space_sensitive_css_display(self) -> bool:
        return False

    @property
    def is_trailing_space_sensitive(self) -> bool:
        if self.type == self.DATA_TAG_NAME and self.next_tag and self.next_tag == self.DATA_TAG_NAME:
            return True

        if not self.parent or self.parent.is_display_none:
            return False

        if self.is_pre:
            return True

        if not self.next_tag and (self.parent.type != self.ROOT_TAG_NAME or self.parent.is_script or not self.parent.is_last_child_trailing_space_sensitive_css_display):
            return False

        if self.next_tag and not self.next_tag.is_prev_trailing_space_sensitive_css_display:
            return False
        return True


    @property
    def is_script(self) -> bool:
        """
        Describe if Tag is assumed as a 'script' element.

        Element script status is determined from the tag name.

        Whatever script status is, if ``Tag._is_html`` is ``False`` this will always
        return ``False``.

        TODO: <template> element should probably be assumed as a script element.

        Returns:
            bool: True if element is assumed as script element else ``False``.
        """
        if self._is_html:
            return self.name in ("script", "style", "svg:style")

        return False

    def __get_tag_name(self) -> Tuple[Optional[str], str]:
        """
        Get HTML element name and its possible namespace.

        Returns:
            tuple: The pair ``namespace, name``, where ``namespace`` can be
            None if no namespace have been found and ``name`` may be
            forced to lowercase if it is a knowed valid HTML element name, else it is
            left unchanged.
        """
        # tags with a namespace
        namespace = None
        tag = self.rawname
        if ":" in self.rawname:
            namespace = self.rawname.split(":")[0]
            tag = (":").join(self.rawname.split(":")[1:])

        if tag.lower() in html_tag_names:
            tag = tag.lower()
        if tag.lower() == "doctype":
            tag = "DOCTYPE"
        return namespace, tag

    @property
    def _attributes(self) -> str:
        """
        Return normalized attributes for a HTML element.

        Normalization is just about lowercase and whitespace divider between multiple
        attributes.

        Returns:
            string: Empty string if there is no attribute or ``None`` if element is not
            HTML (as returned from ``_is_html``). Else it will return a string
            including all the attributes.
        """
        if not self.raw_attributes:
            return ""

        if self._is_html:
            p = AttributeTreeBuilder(self.config, self.raw_attributes, self.tag, self.indent_padding, self.level)
            return p.format()

        # template attributes
        return " " + self.raw_attributes

    def current_indent(self, level):
        """
        Compute final indentation to apply.

        This repeats the indentation string from ``Tag.config.indent`` for each level.
        Zero or negative level will return an empty string.

        Arguments:
            level (integer): Current element level in HTML tree.

        Returns:
            string: Indentation string to apply.
        """
        return level * self.config.indent

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
            s+=child.format(level)

        return s

    @property
    def has_leading_space(self) -> bool:
        return False
    @property
    def should_hug_content(self) -> bool:
        return (
            len(self.children) == 1
            and self.first_child().type in ['curly_two'] # and other statement tags
            and self.first_child().is_leading_space_sensitive
            and not self.first_child().has_leading_space
            and self.last_child().is_trailing_space_sensitive
            and not self.last_child().has_trailing_space
            )


    def print_line_before_children(self) -> str:
        if not self.children:
            return ""

        if self.should_hug_content:
            return ""

        if self.first_child() and self.first_child().has_leading_space and self.first_child().is_leading_space_sensitive:
            return ""

        if self.first_child() and self.first_child().type == self.DATA_TAG_NAME and self.is_whitespace_sensitive and self.is_indentation_sensitive:
            return ""

        print("before!", self.type, self.name)
        return "\n"

    @property
    def needs_to_borrow_prev_closing_tag_end_marker(self) -> bool:
        return False

    def print_line_between_children(self) -> str:
        if self.next_tag and self.next_tag.type in ["open"] and self.type in ["open"] and self.parent.last_child() != self:
            return "\n"
        return ""

    def print_line_after_children(self) -> str:
        if self.type in ["open"] and not self.children:
            return ""

        needs_to_borrow = False
        if self.next_tag:
            needs_to_borrow = self.next_tag.needs_to_borrow_prev_closing_tag_end_marker
        elif self.parent:
            needs_to_borrow = self.parent.needs_to_borrow_prev_closing_tag_end_marker

        if needs_to_borrow:
            if self.last_child() and self.last_child().has_trailing_space and self.last_child().is_trailing_space_sensitive:
                return " "
            return ""

        if self.should_hug_content:
            return ""

        if self.last_child() and self.last_child().has_trailing_space and self.last_child().is_trailing_space_sensitive:
            return "\n"

        if self.last_child() and (self.last_child().type == "comment" or (self.last_child().type == self.DATA_TAG_NAME and self.is_whitespace_sensitive and self.is_indentation_sensitive)):
            return ""

        if self.type == self.DATA_TAG_NAME:
            return ""

        return "\n"

    def format(self, level=0):
        """
        Return formatted element output.

        This will recursively format current element and all of its children.

        Keyword Arguments:
            level (integer): The current element level, it will impact indentation
                width. Default to zero.

        Returns:
            string: Formatted element output.


        methods needed:
        - should_preserver_content
        - ✅ should_hug_content
        - ✅ is_script
        - ✅ needs_to_borrow_prev_closing_tag_end_marker
        - needs_to_borrow_last_child_closing_tag_end_marker
        - needs_to_borrow_parent_closing_tag_start_marker
        - needs_to_borrow_next_opening_tag_start_marker
        - force_not_to_break_attr_content
        - should_print_attribute_per_line
        - print_between_line
        - prefer_hard_line_as_leading_space
        - ✅ is_text_like_node (self.tag == self.DATA_TAG)
        - force_break_children
        - force_next_empty_line
        - print_child


        props:
        - print_break_before_children
        - print_line_after_children
        - ✅ is_front_matter
        - ✅ is_whitespace_sensitive
        - ✅ is_leading_space_sensitive
        - has_leading_space
        - ✅ is_trailing_space_sensitive
        - has_trailing_spaces
        - ✅ is_indentation_sensitive
        - has_dangling_spaces
        - ✅ is_dangling_space_sensitive
        """

        """

        print opening tag
        print children
        print closing tag
        """
        self.level = level
        print(self.name,level)
        open_tag = self.open_tag

        if open_tag and self.tag not in [self.ROOT_TAG_NAME , self.DATA_TAG_NAME]:
            self.output.append(self.current_indent(level) + open_tag)

            if not self.is_void:
                level += 1
                self.output.append(self.print_line_before_children())


        self.output.append("".join(self.data))

        self.output+= self.format_contents(level)

        self.output.append(self.print_line_after_children())

        if not self.is_void:
            level -= 1

        if self.tag not in ["doctype", self.ROOT_TAG_NAME] and self.close_tag:
            if re.match(r"\n", self.output[-1]):
                self.output.append(self.current_indent(level))

            self.output.append(self.close_tag)

        self.output.append(self.print_line_between_children())

        print(self.output)

        return self.output
