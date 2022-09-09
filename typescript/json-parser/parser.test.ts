import assert from 'node:assert/strict';
import { test } from 'node:test';
import { JsonSyntaxError, parseJson } from './parser.ts';

const VALID = [
  '0', '-0', '1.5e-3', '1E+2', '"hi"', 'true', 'false', 'null', '[]', '{}', ' [1, [2, [3]], {"a": null}] ',
  '"\\u00e9\\n\\t\\"\\\\\\/"', '"\\ud83d\\ude00"', '{"__proto__": 1, "a": {"b": [true, false]}}', '123456789012345678901234567890',
];
const INVALID = [
  '', ' ', '01', '1.', '.5', '+1', '1e', '-', 'tru', 'nul', '[1,]', '{"a":1,}', '{a: 1}', "'x'", '"\\x"',
  '"\\u12"', '"a\nb"', '[1 2]', '{"a" 1}', '"open', '[', '{', '1 2', 'NaN', 'Infinity',
];

test('agrees with JSON.parse on valid documents', () => {
  for (const text of VALID) assert.deepEqual(parseJson(text), JSON.parse(text), text);
});

test('keeps "__proto__" as an ordinary key', () => {
  const parsed = parseJson('{"__proto__": {"polluted": true}}') as Record<string, unknown>;
  assert.deepEqual(Object.keys(parsed), ['__proto__']);
  assert.equal(({} as Record<string, unknown>).polluted, undefined);
});

test('rejects what JSON.parse rejects', () => {
  for (const text of INVALID) {
    assert.throws(() => JSON.parse(text), SyntaxError, `JSON.parse accepted ${JSON.stringify(text)}`);
    assert.throws(() => parseJson(text), JsonSyntaxError, JSON.stringify(text));
  }
});

test('reports line and column', () => {
  try {
    parseJson('{\n  "a": 1,\n  "b": tru\n}');
    assert.fail('expected an error');
  } catch (error) {
    assert.ok(error instanceof JsonSyntaxError);
    assert.equal(error.line, 3);
    assert.equal(error.column, 8);
  }
});

test('round-trips random documents built with JSON.stringify', () => {
  let seed = 7;
  const random = () => ((seed = (seed * 48_271) % 2_147_483_647) / 2_147_483_647);
  const build = (depth: number): unknown => {
    const roll = random();
    if (depth === 0 || roll < 0.4) {
      return [null, true, false, Math.round(random() * 1e6) / 100, -random(), 'text ü\u{1F600} "q" \\', ''][Math.floor(random() * 7)];
    }
    if (roll < 0.7) return Array.from({ length: Math.floor(random() * 4) }, () => build(depth - 1));
    return Object.fromEntries(Array.from({ length: Math.floor(random() * 4) }, (_, k) => [`k${k}`, build(depth - 1)]));
  };
  for (let n = 0; n < 300; n += 1) {
    const text = JSON.stringify(build(4), null, n % 2 ? 2 : undefined) ?? 'null';
    assert.deepEqual(parseJson(text), JSON.parse(text));
  }
});

test('limits nesting depth instead of overflowing the stack', () => {
  assert.throws(() => parseJson('['.repeat(10_000) + ']'.repeat(10_000)), /Nesting deeper/);
});
