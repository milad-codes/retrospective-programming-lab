import assert from 'node:assert/strict';
import { test } from 'node:test';
import { calculate } from './evaluate.ts';
import { ExpressionError } from './lexer.ts';
import { format, type Node, parse } from './parser.ts';

test('applies precedence and associativity', () => {
  assert.equal(calculate('1 + 2 * 3'), 7);
  assert.equal(calculate('(1 + 2) * 3'), 9);
  assert.equal(calculate('10 - 4 - 3'), 3);
  assert.equal(calculate('2 ^ 3 ^ 2'), 512);
  assert.equal(calculate('-2 ^ 2'), -4);
  assert.equal(calculate('2 * -3'), -6);
  assert.equal(calculate('7 % 4 + 1'), 4);
});

test('evaluates variables and functions', () => {
  assert.equal(calculate('round(price * (1 + vat), 2)', { price: 19.99, vat: 0.19 }), 23.79);
  assert.equal(calculate('max(1, abs(-7), sqrt(16))'), 7);
});

test('reports errors with positions', () => {
  const position = (source: string, variables = {}) => {
    try {
      calculate(source, variables);
    } catch (error) {
      assert.ok(error instanceof ExpressionError, String(error));
      return error.position;
    }
    assert.fail(`no error for ${source}`);
  };
  assert.equal(position('1 +'), 3);
  assert.equal(position('(1 + 2'), 6);
  assert.equal(position('2 * y'), 4);
  assert.equal(position('nope(1)'), 0);
  assert.equal(position('min()'), 0);
  assert.equal(position('1 2'), 2);
  assert.throws(() => calculate('1 / (2 - 2)'), /Division by zero/);
});

test('format and parse round-trip on random trees', () => {
  let seed = 42;
  const random = () => ((seed = (seed * 1_103_515_245 + 12_345) % 2 ** 31) / 2 ** 31);
  const pick = <T,>(items: readonly T[]): T => items[Math.floor(random() * items.length)]!;
  const tree = (depth: number): Node => {
    const roll = random();
    if (depth === 0 || roll < 0.3) return random() < 0.5 ? { type: 'number', value: Math.floor(random() * 9) + 1 } : { type: 'variable', name: pick(['a', 'b']), position: 0 };
    if (roll < 0.45) return { type: 'unary', operator: '-', operand: tree(depth - 1) };
    return { type: 'binary', operator: pick(['+', '-', '*', '/', '^']), left: tree(depth - 1), right: tree(depth - 1) };
  };
  const strip = (node: Node): unknown => JSON.parse(JSON.stringify(node, (key, value) => (key === 'position' ? undefined : value)));
  for (let i = 0; i < 500; i += 1) {
    const original = tree(4);
    assert.deepEqual(strip(parse(format(original))), strip(original), format(original));
  }
});
