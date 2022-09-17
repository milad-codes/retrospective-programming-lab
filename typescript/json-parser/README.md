# JSON parser

A recursive-descent JSON parser written from the grammar in [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259). It
returns the same values as `JSON.parse` and points at the line and column of the first error:

```text
JsonSyntaxError: Unexpected "t" (line 3, column 8)
```

Details that are easy to get wrong, each covered by a test:

- numbers: `01`, `1.`, `.5`, `+1` and `NaN` are invalid; `-0` and `1E+2` are valid;
- strings: every escape, `\u` escapes including surrogate pairs, and no raw control characters;
- `"__proto__"` becomes an ordinary key, as with `JSON.parse`, instead of changing the object's prototype;
- nesting deeper than 512 levels is an error, not a stack overflow.

The tests compare it with `JSON.parse` on hand-written edge cases and on 300 random documents.

```bash
node --test typescript/json-parser/
```
