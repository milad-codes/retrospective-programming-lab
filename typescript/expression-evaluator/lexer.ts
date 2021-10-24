/** Splits an arithmetic expression into tokens and remembers where each one starts, for error messages. */

export type TokenKind = 'number' | 'name' | 'operator' | 'lparen' | 'rparen' | 'comma' | 'end';

export interface Token {
  kind: TokenKind;
  text: string;
  position: number;
}

export class ExpressionError extends Error {
  readonly position: number;

  constructor(message: string, position: number) {
    super(`${message} at position ${position}`);
    this.name = 'ExpressionError';
    this.position = position;
  }
}

const NUMBER = /(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?/y;
const NAME = /[A-Za-z_][A-Za-z0-9_]*/y;
const PUNCTUATION: Record<string, TokenKind> = { '(': 'lparen', ')': 'rparen', ',': 'comma' };
const OPERATORS = '+-*/%^';

export function tokenize(source: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  while (i < source.length) {
    const char = source[i]!;
    if (/\s/.test(char)) {
      i += 1;
      continue;
    }
    const punctuation = PUNCTUATION[char];
    if (punctuation || OPERATORS.includes(char)) {
      tokens.push({ kind: punctuation ?? 'operator', text: char, position: i });
      i += 1;
      continue;
    }
    let matched = false;
    for (const [pattern, kind] of [
      [NUMBER, 'number'],
      [NAME, 'name'],
    ] as const) {
      pattern.lastIndex = i;
      const match = pattern.exec(source);
      if (match) {
        tokens.push({ kind, text: match[0], position: i });
        i += match[0].length;
        matched = true;
        break;
      }
    }
    if (!matched) throw new ExpressionError(`Unexpected character "${char}"`, i);
  }
  tokens.push({ kind: 'end', text: '', position: source.length });
  return tokens;
}
