"""Build an attribute hierarchy from the
attribute parser output.
"""

from .attribute_parser import AttributeParser
from .attribute_tag import AttributeTag


class AttributeTreeBuilder(AttributeTag):


    def __init__(self, config, text, parent_tag, indent_padding, level):

        self.text = text
        self.config = config
        self.parser = AttributeParser(config, parent_tag, indent_padding)
        self.parent_tag = parent_tag
        self.indent_padding = indent_padding
        self.base_level = level
        self._reset()
        self._feed()


    def _reset(self):
        AttributeTag.__init__(self, self.ROOT_TAG_NAME, self.config, self.parent_tag, self.indent_padding)
        self.parser.reset()
        self.tagStack = []  # children of current tag
        self.current_tag = None
        self._most_recent_tag = None
        self.current_data = []

        self.pushTag(self)

    def _feed(self):
        self.parser.tree = self

        self.parser.feed(self.text)

        while self.current_tag.name != self.ROOT_TAG_NAME:
            self.popTag()

        # self.endData()

    def handle_starttag(self, tag):
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag

        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag)

        return tag

    def popTag(self):
        tag = self.tagStack.pop()

        if self.tagStack:
            self.current_tag = self.tagStack[-1]

        return self.current_tag

    def pushTag(self, tag, stack=True):
        # print("pusing", tag.data, tag.type, tag.raw_attributes)
        if self.current_tag:
            self.current_tag.children.append(tag)

        if stack:
            self.tagStack.append(tag)

            self.current_tag = self.tagStack[-1]

    def _popToTag(self, name, namespace, inclusivePop=True):

        if name == self.ROOT_TAG_NAME:
            return

        last_pop = None

        stack_size = len(self.tagStack)

        for i in range(stack_size - 1, 0, -1):
            t = self.tagStack[i]
            if (
                name == t.name and namespace == t.namespace
            ):  # and t.type = type... curly=curly, html=html etc
                if inclusivePop:
                    last_pop = self.popTag()
                break
            last_pop = self.popTag()

        return last_pop

    def handle_statement(self, tag):
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag

        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag, stack=False)

        return tag

    def handle_endtag(self, tag):

        self._popToTag(tag.name, tag.namespace)
        self.pushTag(tag, stack=False)

    def handle_name(self, data, props):
        # handle strings and space
        self.current_tag.data.append(data)
