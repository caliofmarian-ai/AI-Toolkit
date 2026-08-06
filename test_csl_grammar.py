from python.canonical_parser.lexer import CslLexer

tests = {
    "H1": "# Title",
    "H2": "## Section",
    "H3": "### Subsection",
    "H4": "#### Deep Section",
    "Metadata": "Version: 1.0",
    "Metadata 2": "Status: Draft",
    "Metadata 3": "Owner: Marian",
    "Bullet": "- Item",
    "Nested Bullet": "- Parent\n  - Child",
    "Number": "12345",
    "Identifier": "CANON-999",
    "Quoted String": '"Hello CSL"',
    "Comment": "<!-- comment -->",
    "Separator": "---",
    "Table": "|A|B|\n|1|2|",
    "Code": "```python\nprint('hello')\nx = 1\n```",
}

print("=" * 70)
print("CSL GRAMMAR DISCOVERY TEST")
print("=" * 70)

for name, source in tests.items():
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    lexer = CslLexer(source, name)

    try:
        tokens = lexer.tokenize()
        print("TOKEN COUNT:", len(tokens))
        for token in tokens:
            print(f"{token.token_type.name:20} {repr(token.value)}")
    except Exception as exc:
        print("FAILED:", exc)

print("\n" + "=" * 70)
print("GRAMMAR DISCOVERY FINISHED")
print("=" * 70)
