import markdown
from markdown_macros import (
    sanitize_html, _remove_quotes, find_macros,
    MacroExtension
)

def test_sanitize_html():
    sanitize_html("<b>hello") == "<b>hello</b>"
    sanitize_html("<p>hello, <i>world</p>") == "<p>hello, <i>world</i></p>"

def test_remove_quotes():
    assert _remove_quotes('"hello"') == 'hello'
    assert _remove_quotes("'hello'") == 'hello'
    assert _remove_quotes("hello") == 'hello'

    assert _remove_quotes(" 'hello' ") == 'hello'

def test_find_macros():
    text = """
    Let's look at this example:

    {{ Example("example-id") }}

    And solve this exercise:

    {{ Exercise("exercise-id") }}
    """

    assert find_macros(text) == [
        ("Example", ["example-id"], {}),
        ("Exercise", ["exercise-id"], {})
    ]

def uppercase_macro(value):
    return value.upper()

class TestMacroExtension:
    def render(self, text, **registry):
        extn = MacroExtension(registry=registry)
        return markdown.markdown(text, extensions=[extn])

    def test_uppercase(self):
        text = """
            {{ UpperCase("foobar") }}
        """
        assert self.render(text, UpperCase=uppercase_macro)
