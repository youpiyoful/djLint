"""Build the new html from the old.

A lot of inspiration coming from an older bs4 release.

https://github.com/waylan/beautifulsoup/blob/480367ce8c8a4d1ada3012a95f0b5c2cce4cf497/bs4/__init__.py#L278
https://github.com/waylan/beautifulsoup/blob/master/COPYING.txt

All sections are a tag, even text blocks.

While text continues, it is added to the same block.
node type of text

"""
from .parser import TemplateParser
from .tag import Tag


class TreeBuilder(Tag):
    """Tree Builder takes tags and assembles them into a hierarchy.

    Formatting of the entire html is achieved by iterating the tags and calling tag.format().
    """



    def __init__(self, config, text):
        self.text = text
        self.config = config
        self.parser = TemplateParser(config)
        self._reset()
        self._feed()

    def _reset(self):
        Tag.__init__(self, self.ROOT_TAG_NAME, self.config)
        self.hidden = 1
        self.parser.reset()

        self.tagStack = []  # children of current tag
        self.current_tag = None
        self._most_recent_tag = None
        self.current_data = []

        self.pushTag(self)

    def _feed(self):
        self.parser.tree = self
        self.parser.feed(self.text)
        self.parser.close()

        while self.current_tag.name != self.ROOT_TAG_NAME:
            self.popTag()

        self.endData()

    def endData(self):
        return

    def handle_starttag(self, tag):
        self.endData()

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
        if self.current_tag:
            self.current_tag.children.append(tag)

        if stack:
            self.tagStack.append(tag)

            self.current_tag = self.tagStack[-1]

    def _popToTag(self, name, namespace, inclusivePop=True):

        if name == self.ROOT_TAG_NAME:
            # don't leave me!
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

    def handle_endtag(self, tag):
        """Html tags have no "contents" in the closing tag, so they are not tracked.

        However, we track the closing tag otherwise as their maybe attributes or properties we need to use.
        """
        self.endData()
        self._popToTag(tag.name, tag.namespace)

        if tag.is_html is False:
            # but don't push to stack!
            self.pushTag(tag, stack=False)

    def handle_data(self, data):
        if data.strip() == "":
            self._most_recent_tag.raw_properties.append('has-trailing-space')
            return self._most_recent_tag
        if self._most_recent_tag.type == self.DATA_TAG_NAME:
            self._most_recent_tag.data.append(data)

            return self._most_recent_tag

        tag = Tag(self.DATA_TAG_NAME, self.config)
        tag.type =self.DATA_TAG_NAME
        tag.data.append(data)
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self.pushTag(tag, stack=False)

        return tag


    def handle_statement(self,tag):
        self.endData()
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self.pushTag(tag, stack=False)


    def handle_decl(self, tag):
        self.endData()
        tag.parent = self.current_tag
        tag.previous_tag = self._most_recent_tag
        if self._most_recent_tag:
            self._most_recent_tag.next_tag = tag

        self._most_recent_tag = tag

        self.pushTag(tag)
        self.endData()
        self._popToTag(tag.name, tag.namespace)

        return tag
