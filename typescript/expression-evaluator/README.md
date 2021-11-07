# Expression evaluator

A calculator language in three small stages: a tokenizer, a Pratt parser and a tree-walking evaluator.

```ts
import { calculate } from './evaluate.ts';
calculate('round(price * (1 + vat), 2)', { price: 19.99, vat: 0.19 }); // 23.79
```

| File | Role |
| --- | --- |
| `lexer.ts` | numbers (`2.5e3`, `.5`), names, operators and punctuation, each with its source position |
| `parser.ts` | Pratt parser into a tree; `format` prints a tree back with only the parentheses it needs |
| `evaluate.ts` | evaluation with variables and `abs`, `sqrt`, `min`, `max`, `round(x, digits)`, with arity checks |

Precedence, lowest first: `+ -`, then `* / %`, then unary `-` and `+`, then `^`, which is right-associative. So
`2 ^ 3 ^ 2` is 512 and `-2 ^ 2` is −4, as in mathematics. Every error carries the position of the offending token.

The round-trip test builds 500 random trees, prints them with `format`, parses them again and expects the same tree.
That covers the parenthesisation rules better than hand-written cases.

```bash
node --test typescript/expression-evaluator/   # Node 22.18+ runs TypeScript directly
```
