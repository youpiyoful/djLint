from typing import List

from .tools import Fill, Group, Hardline, Indent, Line, Softline


class Writer:
    def __init__(self, config, indent=-1, current_length=0):
        self.config = config
        self.current_length = current_length
        self.indent = indent

    def write(self, contents, parent=None):

        doc = ""

        # split into chunks by hard breaks
        # then count the length of the chunk
        # if chunk length > max line,
        # then softline = hard break
        # else softline = no break

        current_contents = []

        for x, element in enumerate(contents):
            has_next_element = bool(len(contents) and contents[x + 1 :])
            previous_element = contents[x - 1] if contents[x - 1 :] else None
            if isinstance(element, Hardline):  # hardbreak

                indent = ""

                # if we were the first element, then add the indent for the next
                # if x == 0 and has_next_element:
                #     indent = self.get_indent()
                doc += self.process(current_contents, parent) + element.resolve(
                    indent=indent
                )  # + f"Hardline-{type(parent)}-{type(previous_element)}-{self.indent}\n"

                if isinstance(parent, Indent) and has_next_element:
                    doc += self.get_indent()

                current_contents = []

                continue  # skip rest of loop

            current_contents.append(element)

        doc += self.process(current_contents, parent)

        return doc

    def get_indent(self):
        return self.indent * self.config.indent

    def process(self, current_contents, parent=None):
        doc = ""

        length = sum(len(x) for x in current_contents)

        if length > self.config.max_line_length or isinstance(parent, Indent):
            soft_break_type = "hard"
        else:
            soft_break_type = None

        if length > self.config.max_line_length:
            line_break_type = "hard"
        else:
            line_break_type = None

        for x, element in enumerate(current_contents):
            has_next_element = bool(current_contents[x + 1 :])
            previous_element = current_contents[x - 1] if has_next_element else None
            if isinstance(element, Softline):
                indent = ""

                #     # only add indent if there is another sibling.
                #     indent = self.get_indent()
                # if doc[-1:] and doc[-1] != "\n":
                # print(soft_break_type)
                doc += element.resolve(
                    break_type=soft_break_type, indent=indent
                )  # + f"Softline-{type(parent)}-{type(previous_element)}-{self.indent}\n"

                if isinstance(parent, Indent) and has_next_element:
                    doc += self.get_indent()

            elif isinstance(element, Line):
                indent = ""
                if has_next_element:
                    # only add indent if there is another sibling.
                    indent = self.get_indent()

                doc += element.resolve(
                    break_type=line_break_type, indent=indent, next=has_next_element
                )  # + f"Line-{type(parent)}-{self.indent}\n"

            elif isinstance(element, Indent):
                children = Writer(
                    self.config, self.indent + 1, self.current_length
                ).write(element.get_elements(), element)

                # if children:
                #     doc += self.get_indent()
                doc += children

            elif isinstance(element, List) or isinstance(element, Group):
                doc += Writer(self.config, self.indent, self.current_length).write(
                    element, element
                )

            elif isinstance(element, Fill):
                doc += element.resolve(
                    len(self.get_indent()), self.config.max_line_length
                )

            elif element:
                doc += element

        return doc
