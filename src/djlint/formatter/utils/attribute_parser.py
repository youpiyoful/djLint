"""djlint Attribute Parser Overrides.

This class overrides the AttributeParser functions.

The output elements form AttributeParser are converted into Tag
elements that are then used in the builder.
"""

from HtmlTemplateParser import AttributeParser as Atp

from .attribute_tag import AttributeTag as Tag


class AttributeParser(Atp):
    """Overrides from AttributeParser."""

    DATA_TAG_NAME = "djlint-data"

    def __init__(self, config, parent_tag, indent_padding):
        super(AttributeParser, self).__init__()
        self.config = config
        self.parent_tag = parent_tag
        self.indent_padding = indent_padding
        self.tree = None
        self.tag = Tag("None", self.config, parent_tag)

    def handle_starttag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            indent_padding=self.indent_padding,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_perc"

        self.tree.handle_starttag(self.tag)

    def handle_endtag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            indent_padding=self.indent_padding,
            attributes=attrs,
            properties=props,
        )
        self.tag.type = "endtag_curly_perc"

        self.tree.handle_endtag(self.tag)

    def handle_starttag_comment_curly_perc(self, tag, attrs, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            indent_padding=self.indent_padding,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_comment_curly_perc"

        self.tree.handle_starttag(self.tag)

    def handle_endtag_comment_curly_perc(self, tag, attrs, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            indent_padding=self.indent_padding,
            properties=props,
        )
        self.tag.type = "endtag_comment_curly_perc"

        self.tree.handle_endtag(self.tag)

    def handle_comment_curly_hash(self, value):
        # django/jinja comment
        tag = Tag(value, self.config, self.parent_tag,indent_padding=self.indent_padding,)
        tag.type = "comment_curly_hash"

        self.handle_statement(tag, None)

    def handle_comment_curly_two_exclaim(self, value, props):
        # handlebars comment
        tag = Tag(value, self.config,self.parent_tag, indent_padding=self.indent_padding,properties=props)
        tag.type = "curly_two_exlaim"

        self.handle_statement(tag, None)

    def handle_comment_at_star(self, value):
        # c# razor pages comment
        tag = Tag(value, self.config,self.parent_tag,indent_padding=self.indent_padding,)
        tag.type = "comment_at_star"

        self.handle_statement(tag, None)

    def handle_starttag_curly_two_hash(self, tag, attrs, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            indent_padding=self.indent_padding,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_two_hash"

        self.tree.handle_starttag(self.tag)

    def handle_endtag_curly_two_slash(self, tag, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(tag, self.config,
            self.parent_tag,indent_padding=self.indent_padding, properties=props)
        self.tag.type = "endtag_curly_two_slash"

        self.tree.handle_endtag(self.tag)

    def handle_slash_curly_two(self, tag, attrs):
        # handlebars/mustache inline raw block
        tag = Tag(tag, self.config,
            self.parent_tag,indent_padding=self.indent_padding, attributes=attrs)
        tag.type = "slash_curly_two"

        self.tree.handle_statement(tag)

    def handle_endtag_curly_four_slash(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(tag, self.config,self.parent_tag, indent_padding=self.indent_padding,attributes=attrs, properties=props)
        self.tag.type = "endtag_curly_four_slash"
        self.tree.handle_endtag(self.tag)

    def handle_starttag_curly_four(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(
            tag,
            self.config,
            self.parent_tag,
            indent_padding=self.indent_padding,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_four"

        self.tree.handle_starttag(self.tag)

    def handle_curly_three(self, value):
        # handlebars un-escaped html
        tag = Tag(value, self.config,self.parent_tag,indent_padding=self.indent_padding,)
        tag.type = "curly_three"

        self.tree.handle_statement(tag)

    def handle_curly_two(self, tag, attrs, props):
        tag = Tag(tag, self.config,self.parent_tag,indent_padding=self.indent_padding, attributes=attrs, properties=props)
        tag.type = "curly_two"
        self.tree.handle_statement(tag)

    def handle_name(self, name, props):
        """
        Any free text. If the attribute
        has a value following, there will be a property "has-value".
        """
        tag = Tag(self.DATA_TAG_NAME,self.config,self.parent_tag, indent_padding=self.indent_padding, properties=props)
        tag.type=self.DATA_TAG_NAME
        tag.data.append(name)

        self.tree.handle_statement(tag)

    def handle_value_start(self):
        """
        This will be a quote character where an attribute value starts/ends.
        """
        if self.get_element_text() == "\"":
            self.tree._most_recent_tag.properties.append("has-value-start-double")
        else:
            self.tree._most_recent_tag.properties.append("has-value-start-single")

    def handle_space(self):
        """
        Any whitespace inside an attribute.
        """
        self.tree._most_recent_tag.properties.append("has-trailing-space")
        # pass
