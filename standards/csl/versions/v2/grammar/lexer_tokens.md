# CSL v2 — Lexer Tokens

Identifier: CSL-001-TOKENS  
Version: 2.0.0  
Status: Normative  
Classification: Canonical Standard  
Depends: CSL-001_ENGINEERING_ALPHABET, csl_v2.ebnf §1

---

## 1. Purpose

This document defines the complete engineering vocabulary of CSL v2: every
token category, its lexical pattern, and its role in the language.  It is the
normative reference for implementors of the CSL lexer (CSL-013).

---

## 2. Encoding

| Property          | Value                   |
|-------------------|-------------------------|
| Encoding          | UTF-8 without BOM       |
| Line ending input | LF or CRLF (normalised to LF by lexer) |
| File extension    | `.csl`                  |
| Indentation unit  | 4 spaces (tabs are a lexical error) |

---

## 3. Token Categories

### 3.1 WHITESPACE

Pattern: one or more space (U+0020), horizontal tab (U+0009),
carriage return (U+000D), or line feed (U+000A) characters.

Disposition: consumed and discarded by the lexer.  Indentation-significant
whitespace is converted to INDENT / DEDENT tokens before discard.

### 3.2 NEWLINE

Pattern: `\r\n` or `\n`.

Disposition: emitted as a distinct token at statement boundaries; discarded
inside expressions.

### 3.3 LINE_COMMENT

Pattern: `#` followed by any characters up to (but not including) NEWLINE.

Disposition: consumed by the lexer; may be preserved as trivia tokens for
tooling (formatters, documentation generators).

### 3.4 BLOCK_COMMENT

Pattern: `(*` … `*)`, nestable.

Disposition: same as LINE_COMMENT.

### 3.5 IDENTIFIER

Pattern: `[A-Za-z][A-Za-z0-9\-_]*`

Rules:
- MUST begin with an ASCII letter.
- MUST NOT be identical to a reserved keyword (case-sensitive).
- Case-sensitive: `MyEntity` ≠ `myentity`.
- Minimum length: 1 character.
- Recommended maximum length: 128 characters (implementations MUST support at least 128).

### 3.6 QNAME (Qualified Name)

Pattern: `IDENTIFIER ( "." IDENTIFIER )*`

Used for namespace-qualified references.  Example: `core.security.Policy`.

### 3.7 STRING

Pattern: `"` `STRING_CHAR*` `"`

Escape sequences:

| Sequence | Unicode       |
|----------|---------------|
| `\"`     | U+0022 (")    |
| `\\`     | U+005C (\\)   |
| `\n`     | U+000A (LF)   |
| `\r`     | U+000D (CR)   |
| `\t`     | U+0009 (TAB)  |
| `\uXXXX` | Unicode code point XXXX (4 hex digits) |

Strings MUST NOT contain unescaped `"` or bare newlines.

### 3.8 INTEGER

Pattern: `[-]?[0-9]+`

Range: unbounded (implementations MUST support at least signed 64-bit).

### 3.9 DECIMAL

Pattern: `[-]?[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?`

### 3.10 BOOLEAN

Literals: `true` | `false` (case-sensitive, reserved).

### 3.11 NULL_LITERAL

Literal: `null` (case-sensitive, reserved).

### 3.12 DATE

Pattern: `YYYY-MM-DD` (ISO 8601, Gregorian calendar).

### 3.13 TIMESTAMP

Pattern: `YYYY-MM-DDTHH:MM:SS[.fff][Z|(+|-)HH:MM]` (ISO 8601).

### 3.14 DURATION

Pattern: `[-]?[0-9]+(d|h|m|s)`

| Suffix | Unit    |
|--------|---------|
| `d`    | days    |
| `h`    | hours   |
| `m`    | minutes |
| `s`    | seconds |

Compound durations (e.g., `1d12h`) are composed as a list value, not a single
token.

### 3.15 VERSION_LIT

Pattern: semver-compatible `MAJOR.MINOR.PATCH[-pre][+build]`

Examples: `2.0.0`, `2.0.0-alpha.1`, `2.0.0+20260801`.

### 3.16 INDENT / DEDENT

Virtual tokens emitted by the lexer when the indentation level increases
(INDENT) or decreases (DEDENT) relative to the previous non-blank line.

Rules:
- One indentation level = 4 spaces.
- Tabs in indentation context are a lexical error (CSL-LEX-001).
- Mixed spaces/tabs on the same line are a lexical error (CSL-LEX-002).
- A DEDENT that does not align to a previous INDENT level is a lexical error
  (CSL-LEX-003).

### 3.17 OPERATORS

| Token | Symbol | Context                        |
|-------|--------|--------------------------------|
| EQ    | `=`    | comparison, alias assignment   |
| NEQ   | `!=`   | comparison                     |
| LT    | `<`    | comparison                     |
| LTE   | `<=`   | comparison                     |
| GT    | `>`    | comparison                     |
| GTE   | `>=`   | comparison                     |
| ARROW | `=>`   | future: lambda / mapping       |
| AT    | `@`    | version pinning in entity refs |

### 3.18 DELIMITERS

| Token    | Symbol | Context                    |
|----------|--------|----------------------------|
| LBRACE   | `{`    | map literals               |
| RBRACE   | `}`    | map literals               |
| LPAREN   | `(`    | grouping, type params      |
| RPAREN   | `)`    | grouping, type params      |
| LBRACKET | `[`    | list literals, type params |
| RBRACKET | `]`    | list literals, type params |
| COLON    | `:`    | field assignment           |
| COMMA    | `,`    | element separator          |
| DOT      | `.`    | qualified name separator   |
| PIPE     | `\|`   | multiline string marker    |
| DASH     | `-`    | list item marker           |
| SEMICOLON| `;`    | reserved (future use)      |
| QUESTION | `?`    | reserved (future use)      |
| BANG     | `!`    | negation operator prefix   |

### 3.19 EOF

A virtual token marking the end of the input stream.

---

## 4. Tokenisation Precedence

When multiple patterns could match at the same position, the lexer applies
longest-match first, then keyword precedence over IDENTIFIER:

1. Keyword (exact case-sensitive match from §2 of `csl_v2.ebnf`)
2. `true` / `false` / `null` (boolean / null literals)
3. TIMESTAMP (tried before DATE because it is longer)
4. DATE
5. DECIMAL (tried before INTEGER because it contains a dot)
6. INTEGER
7. DURATION
8. VERSION_LIT
9. IDENTIFIER / QNAME
10. STRING
11. Operator / Delimiter (longest token first)

---

## 5. Error Token

When the lexer encounters an unrecognised character sequence it emits an
`ERROR` token carrying:

- `source_span` — start line, start column, end line, end column
- `raw_text`    — the offending character(s)
- `diagnostic`  — CSL-LEX-000 (unrecognised input)

The lexer SHALL attempt to recover and continue tokenising after emitting an
ERROR token.

---

*End of lexer_tokens.md — CSL-001-TOKENS v2.0.0*
