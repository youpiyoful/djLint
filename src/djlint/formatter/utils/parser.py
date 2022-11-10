"""djLint Html Template Parser Overrides

This class overrides the HtmlTemplateParser functions.

The output elements from HtmlTemplateParser are converted into Tag
elements that are then used in the builder.
"""

import re
from typing import Dict, List, Optional, Tuple

from HtmlTemplateParser import Htp

from .tag import Tag


class TemplateParser(Htp):
    """Overrides for HtmlTemplateParser."""


    def __init__(self, config):

        super(TemplateParser, self).__init__()

        self.config = config
        self.tree = None
        # self.last_sibling: Optional[Tag] = None
        # self.last_parent: Optional[Tag] = None
        self.tag = Tag("None", self.config)
        # self.parents = []

    # def get_parent(self):
    #     if len(self.parents) > 0:
    #         return self.parents[-1]
    #     return None

    def handle_decl(self, decl: str) -> None:

        if re.match(r"doctype", decl, re.I):

            decl = re.sub(r"^doctype", "", decl, flags=re.I | re.M).strip()

            self.tag = Tag(
                "doctype",
                self.config,
                # parent=self.last_parent,
                attributes=decl,
            )
            self.tag.is_html = True
            self.tree.handle_decl(self.tag)

    def handle_starttag(self, tag: str, attrs: str, props: List) -> None:
        """Handle start tag.

        Create a tag object.

        If the tag is not void, update last parent.
        """
        # if self.tag.type == "open":
        #     self.last_sibling = self.tag

        self.tag = Tag(tag, self.config, attributes=attrs, properties=props)
        self.tag.is_html = True

        if not self.tag.is_void:
            self.tag.type = "open"
        else:
            self.tag.type = "void"

        self.tree.handle_starttag(self.tag)

    def handle_starttag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_perc"

        self.tree.handle_starttag(self.tag)

    def handle_starttag_curly_four(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )
        self.tag.set_profile("handlebars")
        self.tag.type = "starttag_curly_four"

        self.tree.handle_starttag(self.tag)

    def handle_starttag_curly_two_hash(self, tag, attrs, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )
        self.tag.set_profile("handlebars")
        self.tag.type = "starttag_curly_two_hash"

        self.tree.handle_starttag(self.tag)

    def handle_starttag_comment_curly_perc(self, data, attrs, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_comment_curly_perc"

        self.tree.handle_starttag(self.tag)

    def handle_endtag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )
        self.tag.type = "endtag_curly_perc"

        self.tree.handle_endtag(self.tag)

        # self.last_sibling = self.tag
        # self.last_parent = self.get_open_parent(self.tag.parent)

    def handle_endtag_curly_two_slash(self, tag, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(tag, self.config, properties=props)
        self.tag.set_profile("handlebars")
        self.tag.type = "endtag_curly_two_slash"
        self.tree.handle_endtag(self.tag)

    def handle_endtag_curly_four_slash(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(tag, self.config, attributes=attrs, properties=props)
        self.tag.set_profile("handlebars")
        self.tag.type = "endtag_curly_four_slash"

        self.tree.handle_endtag(self.tag)

    def handle_comment_curly_hash(self, data):
        # django/jinja comment
        tag = Tag(data, self.config)
        tag.type = "comment_curly_hash"

        self.handle_statement(tag)

    def handle_comment_at_star(self, data):
        # c# razor pages comment
        tag = Tag(data, self.config)
        tag.type = "comment_at_star"

        self.handle_statement(tag)

    def handle_endtag_comment_curly_perc(self, tag, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
            properties=props,
        )
        self.tag.type = "endtag_comment_curly_perc"

        self.tree.handle_endtag(self.tag)

    def handle_comment_curly_two_exlaim(self, data, props):
        # handlebars comment
        tag = Tag(data, self.config, properties=props)
        tag.set_profile("handlebars")
        self.tag.set_profile("handlebars")
        tag.type = "curly_two_exlaim"

        self.tree.handle_statement(tag)

    def handle_charref(self, data):
        print("charref", data)

    def handle_entityref(self, data):
        print("entityref", data)

    def handle_pi(self, data):
        # handle processing instruction
        print("pi", data)

    def unknown_decl(self, decl):
        print("unknown decl", decl)

    def handle_endtag(self, tag: str) -> None:
        """Handle end tag.

        Create a tag object. Do not update the class property
        unless it is not a void tag.

        If the tag is not void, update the last sibling.
        """
        close_tag = Tag(tag, self.config)  # , parent=self.last_parent)
        close_tag.type = "close"
        close_tag.is_html = True

        if not close_tag.is_void:

            self.tag = close_tag

            self.tree.handle_endtag(self.tag)
        else:
            # void tags are handled in the open tag block.
            return

    def handle_curly_two(self, data, attrs, props):
        # curly handles as data. build the tag and pass it to the
        # data processor.
        tag = Tag(data, self.config, attributes=attrs, properties=props)
        tag.type = "curly_two"

        self.tree.handle_statement(tag)

    def handle_slash_curly_two(self, data, attrs):
        # handlebars/mustache inline raw block
        tag = Tag(data, self.config, attributes=attrs)
        tag.type = "slash_curly_two"
        self.tag.set_profile("handlebars")
        tag.set_profile("handlebars")

        self.tree.handle_statement(tag)

    def handle_curly_three(self, data):
        # handlebars un-escaped html
        tag = Tag(data, self.config)
        tag.type = "curly_three"
        self.tag.set_profile("handlebars")
        tag.set_profile("handlebars")

        self.tree.handle_statement(tag)

    def handle_data(self, data: str) -> None:
        self.tree.handle_data(data)

    # def handle_startendtag(self, tag, attrs, props):
    #     # start and end of tag <p/>
    #     self.handle_starttag(tag, attrs, props)
    #     self.handle_endtag(tag)

    def handle_comment(self, data: str) -> None:
        # comment <!-- -->
        tag = Tag(
            data,
            self.config,
        )
        tag.type = "comment"
        tag.is_html = True
        self.tree.handle_statement(tag)

    def close(self):
        super(TemplateParser, self).close()
