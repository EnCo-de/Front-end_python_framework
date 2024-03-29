from abc import ABC, abstractmethod

class EmptyElement(ABC):
    def __init__(self, arg_str='', **kwargs):
        s = ''
        for key, value in kwargs.items():
            s += f' {key}="{value}"' if value != '' and value is not None else f' {key}'
        self.arg_str = arg_str + s

    def __str__(self) -> str:
        args = ' ' + self.arg_str if self.arg_str != '' else ''
        return f'<{self.tag_name}{args}>'
    
    @abstractmethod
    def dump(self):
        pass 


class Element(EmptyElement):
    def __init__(self, *contents, arg_str='', **kwargs):
        super(Element, self).__init__(arg_str, **kwargs)
        self.content = list(contents) or []

    def __str__(self) -> str:
        start_tag = super(Element, self).__str__()
        content = '\n'.join(map(str, self.content))
        return start_tag + '\n' + content + f'\n</{self.tag_name}>'
    
    def dump(self):
        args = ' ' + self.arg_str if self.arg_str != '' else ''
        content = '\n'.join([c.dump() for c in self.content])
        return f'<{self.tag_name}{args}>\n  {content}\n</{self.tag_name}>'


class Img(EmptyElement):
    tag_name = 'img'
    
    def dump(self):
        args = ' ' + self.arg_str if self.arg_str != '' else ''
        return f'<{self.tag_name}{args}>'


class Div(Element):
    tag_name = 'div'


class Nav(Div):
    tag_name = 'nav'


class Footer(Div):
    tag_name = 'footer'


class Flex(Div):
    def __init__(self, *contents, arg_str='', **kwargs):
        arg_str += ' style="display:flex; flex-wrap: wrap;"'
        super(Flex, self).__init__(*contents, arg_str=arg_str, **kwargs)


class Li(Element):
    tag_name = 'li'


class Ul(Div):
    tag_name = 'ul'

    def __init__(self, *contents, arg_str='', **kwargs):
        self.lis = [Li(text) for text in contents]
        super(Div, self).__init__(*self.lis, arg_str=arg_str, **kwargs)


class Ol(Ul):
    tag_name = 'ol'


class Span(Element):
    tag_name = 'span'


class Anch(Span):
    tag_name = 'a'

    def __init__(self, href = '#', *contents, arg_str='', **kwargs):
        arg_str = f' href="{href}" ' + arg_str
        super(Anch, self).__init__(*contents, arg_str=arg_str, **kwargs)
        self.href = href


class Pgf(Span):
    tag_name = 'p'


class H1(Span):
    tag_name = 'h1'


if __name__ == '__main__':
    elt = Div()
    inner = Div()
    line = Pgf('very', 'well') 
    san = Span('hello world')
    inner.content.append('some text')
    inner.content.append(san)
    elt.content = [inner, inner, line, 'text']
    m = Img(arg_str='src="https://i.pinimg.com/originals/1c/c2/05/1cc205be895a94383fcb250d80c77591.jpg" alt="alt"')
    inner.content.extend((m,line))


    print(elt)
