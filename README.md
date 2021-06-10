# Macros Extension for Markdown

The markdown_macros is [Python-Markdown][1] extension that defines a markup
for including macros in the markdown text.

[1]: https://python-markdown.github.io/

# Markup

Each macro corresponds to an external function and they are specified
using the following markup:

```
{{ MacroName("macro-argument") }}
```

Currently it only supports one string argument. Support for multiple
arguments and keyword arguments is expected in the next version.

This is typically used to include custom content from external sources.

```
Welcome to the awesome course!

{{ YouTubeVideo("video-id") }}

Let's look at the an example:

{{ Example("example-id") }}

And an exercise:

{{ Exercise("exercise-id") }}
```

In the above example `YouTubeVideo`, `Example` and `Exercise` were the
names of the macros and the the text in the parenthesis is the argument
to the macro.

As of now this extension only supports one argument and that must be a
string.

## Example

The MacroExtension class takes a dictionary of macros, mapping from macro
name to the corresponding function as argument.

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

## License

This repository has been released under the MIT License.

