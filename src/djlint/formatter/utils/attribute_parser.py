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

    def __init__(self, config):
        super(AttributeParser, self).__init__()
        self.config = config
        self.tree = None
        self.tag = Tag("None", self.config)

    def handle_starttag_curly_perc(self, tag, attrs, props):
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_perc"

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

    def handle_starttag_comment_curly_perc(self, tag, attrs, props):
        # django multi line comment {% comment %}{% endcomment %}
        self.tag = Tag(
            tag,
            self.config,
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
            properties=props,
        )
        self.tag.type = "endtag_comment_curly_perc"

        self.tree.handle_endtag(self.tag)

    def handle_comment_curly_hash(self, value):
        # django/jinja comment
        tag = Tag(data, self.config)
        tag.type = "comment_curly_hash"

        self.handle_name(tag.statement_tag)

    def handle_comment_curly_two_exclaim(self, value, props):
        # handlebars comment
        tag = Tag(data, self.config, properties=props)
        tag.type = "curly_two_exlaim"

        self.handle_name(tag.statement_tag)

    def handle_comment_at_star(self, value):
        # c# razor pages comment
        tag = Tag(data, self.config)
        tag.type = "comment_at_star"

        self.handle_name(tag.statement_tag)

    def handle_starttag_curly_two_hash(self, tag, attrs, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        print("here", tag, attrs, props)
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_two_hash"

        self.tree.handle_starttag(self.tag)

    def handle_endtag_curly_two_slash(self, tag, props):
        # handlebars/mustache loop {{#name attributes}}{{/name}}
        self.tag = Tag(tag, self.config, properties=props)
        self.tag.type = "endtag_curly_two_slash"

        self.tree.handle_endtag(self.tag)

    def handle_slash_curly_two(self, tag, attrs):
        # handlebars/mustache inline raw block
        tag = Tag(data, self.config, attributes=attrs)
        tag.type = "slash_curly_two"

        self.tree.handle_name(tag.statement_tag, None)

    def handle_endtag_curly_four_slash(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(tag, self.config, attributes=attrs, properties=props)
        self.tag.type = "endtag_curly_four_slash"

        self.tree.handle_endtag(self.tag)

    def handle_starttag_curly_four(self, tag, attrs, props):
        # handlebars raw close {{{{raw}}}}{{{{/raw}}}}
        self.tag = Tag(
            tag,
            self.config,
            attributes=attrs,
            properties=props,
        )

        self.tag.type = "starttag_curly_four"

        self.tree.handle_starttag(self.tag)

    def handle_curly_three(self, value):
        # handlebars un-escaped html
        tag = Tag(data, self.config)
        tag.type = "curly_three"

        self.tree.handle_name(tag.statement_tag, None)

    def handle_curly_two(self, tag, attrs, props):
        tag = Tag(tag, self.config, attributes=attrs, properties=props)
        tag.type = "curly_two"
        self.tree.handle_name(tag.statement_tag, props)

    def handle_name(self, name, props):
        """
        Any free text. If the attribute
        has a value following, there will be a property "has-value".
        """
        tag = Tag(self.DATA_TAG_NAME, self.config, properties=props)
        tag.data.append(name)

        self.tree.pushTag(tag)

    def handle_value_start(self):
        """
        This will be a quote character where an attribute value starts/ends.
        """
        pass

    def handle_space(self):
        """
        Any whitespace inside an attribute.
        """
        pass
