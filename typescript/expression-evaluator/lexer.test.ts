import assert from 'node:assert/strict';
import { test } from 'node:test';
import { ExpressionError, tokenize } from './lexer.ts';

test('tokenizes numbers, names, operators and punctuation with positions', () => {
  const tokens = tokenize('max(2.5e3, x_1) * -.5');
  assert.deepEqual(
    tokens.map((t) => [t.kind, t.text, t.position]),
    [
      ['name', 'max', 0],
      ['lparen', '(', 3],
      ['number', '2.5e3', 4],
      ['comma', ',', 9],
      ['name', 'x_1', 11],
      ['rparen', ')', 14],
      ['operator', '*', 16],
      ['operator', '-', 18],
      ['number', '.5', 19],
      ['end', '', 21],
    ],
  );
});

test('reports the position of an unexpected character', () => {
  assert.throws(() => tokenize('1 + $'), (error: unknown) => error instanceof ExpressionError && error.position === 4);
});
