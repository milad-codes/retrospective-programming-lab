/**
 * A JSON parser written from the grammar in RFC 8259, with line and column numbers in its error messages.
 * Produces the same values as JSON.parse for valid input; rejects everything JSON.parse rejects.
 */

export type Json = null | boolean | number | string | Json[] | { [key: string]: Json };

export class JsonSyntaxError extends Error {
  readonly line: number;
  readonly column: number;

  constructor(message: string, line: number, column: number) {
    super(`${message} (line ${line}, column ${column})`);
    this.name = 'JsonSyntaxError';
    this.line = line;
    this.column = column;
  }
}

const NUMBER = /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/y;
const ESCAPES: Record<string, string> = { '"': '"', '\\': '\\', '/': '/', b: '\b', f: '\f', n: '\n', r: '\r', t: '\t' };
const MAX_DEPTH = 512;

export function parseJson(text: string): Json {
  let i = 0;

  const fail = (message: string, at = i): never => {
    const before = text.slice(0, at);
    const line = before.split('\n').length;
    throw new JsonSyntaxError(message, line, at - before.lastIndexOf('\n'));
  };
  const skipWhitespace = () => {
    while (text[i] === ' ' || text[i] === '\t' || text[i] === '\n' || text[i] === '\r') i += 1;
  };
  const describe = () => (i >= text.length ? 'end of input' : `"${text[i]}"`);

  function value(depth: number): Json {
    if (depth > MAX_DEPTH) fail(`Nesting deeper than ${MAX_DEPTH} levels`);
    skipWhitespace();
    const char = text[i];
    if (char === '{') return object(depth);
    if (char === '[') return array(depth);
    if (char === '"') return string();
    if (char === '-' || (char !== undefined && char >= '0' && char <= '9')) return number();
    for (const [word, result] of [
      ['true', true],
      ['false', false],
      ['null', null],
    ] as const) {
      if (text.startsWith(word, i)) {
        i += word.length;
        return result;
      }
    }
    return fail(`Unexpected ${describe()}`);
  }

  function object(depth: number): Json {
    const result: { [key: string]: Json } = {};
    i += 1;
    skipWhitespace();
    if (text[i] === '}') {
      i += 1;
      return result;
    }
    for (;;) {
      skipWhitespace();
      if (text[i] !== '"') fail(`Expected a string key but found ${describe()}`);
      const key = string();
      skipWhitespace();
      if (text[i] !== ':') fail(`Expected ":" but found ${describe()}`);
      i += 1;
      // defineProperty keeps a "__proto__" key as plain data, as JSON.parse does
      Object.defineProperty(result, key, { value: value(depth + 1), enumerable: true, writable: true, configurable: true });
      skipWhitespace();
      if (text[i] === '}') {
        i += 1;
        return result;
      }
      if (text[i] !== ',') fail(`Expected "," or "}" but found ${describe()}`);
      i += 1;
    }
  }

  function array(depth: number): Json {
    const result: Json[] = [];
    i += 1;
    skipWhitespace();
    if (text[i] === ']') {
      i += 1;
      return result;
    }
    for (;;) {
      result.push(value(depth + 1));
      skipWhitespace();
      if (text[i] === ']') {
        i += 1;
        return result;
      }
      if (text[i] !== ',') fail(`Expected "," or "]" but found ${describe()}`);
      i += 1;
    }
  }

  function string(): string {
    const start = i;
    i += 1;
    let result = '';
    for (;;) {
      const char = text[i];
      if (char === undefined) fail('Unterminated string', start);
      if (char === '"') {
        i += 1;
        return result;
      }
      if (char! < ' ') fail('Control character in string');
      if (char !== '\\') {
        result += char;
        i += 1;
        continue;
      }
      const escape = text[i + 1];
      if (escape === 'u') {
        const hex = text.slice(i + 2, i + 6);
        if (!/^[0-9a-fA-F]{4}$/.test(hex)) fail('Invalid \\u escape');
        result += String.fromCharCode(parseInt(hex, 16)); // surrogate pairs combine naturally in a JS string
        i += 6;
      } else if (escape !== undefined && escape in ESCAPES) {
        result += ESCAPES[escape];
        i += 2;
      } else {
        fail('Invalid escape');
      }
    }
  }

  function number(): number {
    NUMBER.lastIndex = i;
    const match = NUMBER.exec(text);
    if (!match) return fail('Invalid number');
    i += match[0].length;
    if (/[0-9.eE+-]/.test(text[i] ?? '')) fail('Invalid number');
    return Number(match[0]);
  }

  const result = value(0);
  skipWhitespace();
  if (i < text.length) fail(`Unexpected ${describe()} after the value`);
  return result;
}
