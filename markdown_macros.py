"""
The markdown_macros is Python-Markdown extension that defines a markup
for including macros in the markdown text.

MARKUP

Each macro corresponds to an external function and they are specified
using the following markup:

```
{{ MacroName("macro-argument") }}
```

Currently it only supports one string argument. Support for multiple
arguments and keyword arguments is expected in the next version.

EXAMPLE

The MacroExtension class takes a dictionary of macros, mapping from macro
name to the macro function as argument.

```
import markdown
from markdown_macros import MacroExtension

def hello_macro(name):
    return f"Hello, {name}!"

MACROS = {
    "Hello": hello_macro
}

text = '''Demo of Markdown-Macros.
{{ Hello("Markdown") }}
'''

extn = MacroExtension(registry=MACROS)
html = markdown.markdown(text, extensions=[extn])

// prints:
//    Demo pf Markdown-Macros
//    Hello, Markdown!
print(html)
```
"""
import re
import importlib

from markdown import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup

__version__ = "0.1.0"
__author__ = "Anand Chitipothu <anand@fossunited.org>"

MACRO_RE = r'{{ *(\w+)\(([^{}]*)\) *}}'

class MacroExtension(Extension):
    """MacroExtension is a markdown extension to support macro syntax.
    """
    def __init__(self, **kwargs):
        self.config = {
            'registry' : [{}, 'a dictionary mapping from macro names to corresponding function'],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        self.md = md
        pattern = MacroInlineProcessor(MACRO_RE, self.get_registry())
        pattern.md = md
        md.inlinePatterns.register(pattern, 'macro', 75)

    def get_registry(self):
        config = self.getConfigs()
        def process_value(value):
            if isinstance(value, str):
                return self.load_function(value)
            else:
                return value
        return {k: process_value(v) for k, v in config['registry'].items()}

    def load_function(self, qualified_name):
        """Loads a function from its name.

            >>> load_function("os.path:exists")
            <function exists at 0x10ab3dd40>
        """
        modname, funcname = qualified_name.split(":", 1)
        mod = importlib.import_module(modname)
        return getattr(mod, funcname)

class MacroInlineProcessor(InlineProcessor):
    """MacroInlineProcessor is class that is handles the logic
    of how to render each macro occurence in the markdown text.
    """
    def __init__(self, pattern, registry):
        super().__init__(pattern)
        self.registry = registry

    def handleMatch(self, m, data):
        """Handles each macro match and return rendered contents
        for that macro as an etree node.
        """
        macro = m.group(1)
        arg = m.group(2)
        html = self.render_macro(macro, arg)
        html = sanitize_html(str(html))
        e = etree.fromstring(html)
        return e, m.start(0), m.end(0)

    def render_macro(self, macro_name, macro_argument):
        # stripping the quotes on either side of the argument
        macro_argument = _remove_quotes(macro_argument)

        if macro_name in self.registry:
            return self.registry[macro_name](macro_argument)
        else:
            return f"<p>Unknown macro: {macro_name}</p>"

def find_macros(text):
    """Finds all macros in the given text.

    Returns the macro name, args and keyword arguments.

    Even though currently this library supports only one argument, the
    return format is generalized to support future needs.

        >>> find_macros(text)
        [
            ('YouTubeVideo', ['abcd1234'], {}),
            ('Exercise', ['two-circles'], {}),
            ('Exercise', ['four-circles'], {})
        ]
    """
    macros = re.findall(MACRO_RE, text)
    # remove the quotes around the argument
    return [(name, [_remove_quotes(arg)], {}) for name, arg in macros]

def _remove_quotes(value):
    """Removes quotes around a value.

    Also strips the whitespace.

        >>> _remove_quotes('"hello"')
        'hello'
        >>> _remove_quotes("'hello'")
        'hello'
        >>> _remove_quotes("hello")
        'hello'
    """
    return value.strip(" '\"")

def sanitize_html(html):
    """Sanotize the html using BeautifulSoup.

    The markdown processor request the correct markup and crashes on
    any broken tags. This makes sures that all those things are fixed
    before passing to the etree parser.
    """
    soup = BeautifulSoup(html, features="lxml")
    nodes = soup.body.children
    return "<div>" + "\n".join(str(node) for node in nodes) + "</div>"

