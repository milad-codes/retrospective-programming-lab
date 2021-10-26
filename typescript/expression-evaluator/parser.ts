/**
 * Pratt (precedence-climbing) parser for arithmetic with variables and function calls.
 * Precedence, lowest first: + - · * / % · unary - + · ^ (right-associative), so -2^2 is -(2^2) as in maths.
 */
import { ExpressionError, type Token, tokenize } from './lexer.ts';

export type Node =
  | { type: 'number'; value: number }
  | { type: 'variable'; name: string; position: number }
  | { type: 'unary'; operator: '-' | '+'; operand: Node }
  | { type: 'binary'; operator: string; left: Node; right: Node }
  | { type: 'call'; name: string; args: Node[]; position: number };

const BINARY: Record<string, { precedence: number; rightAssociative: boolean }> = {
  '+': { precedence: 10, rightAssociative: false },
  '-': { precedence: 10, rightAssociative: false },
  '*': { precedence: 20, rightAssociative: false },
  '/': { precedence: 20, rightAssociative: false },
  '%': { precedence: 20, rightAssociative: false },
  '^': { precedence: 40, rightAssociative: true },
};
const UNARY_PRECEDENCE = 30;

export function parse(source: string): Node {
  const tokens = tokenize(source);
  let index = 0;
  const peek = (): Token => tokens[index]!;
  const next = (): Token => tokens[index++]!;
  const expect = (kind: Token['kind'], what: string): Token => {
    const token = next();
    if (token.kind !== kind) throw new ExpressionError(`Expected ${what} but found ${describe(token)}`, token.position);
    return token;
  };

  function expression(minPrecedence: number): Node {
    let left = prefix();
    for (;;) {
      const token = peek();
      const info = token.kind === 'operator' ? BINARY[token.text] : undefined;
      if (!info || info.precedence < minPrecedence) return left;
      next();
      const right = expression(info.rightAssociative ? info.precedence : info.precedence + 1);
      left = { type: 'binary', operator: token.text, left, right };
    }
  }

  function prefix(): Node {
    const token = next();
    switch (token.kind) {
      case 'number':
        return { type: 'number', value: Number(token.text) };
      case 'name':
        if (peek().kind !== 'lparen') return { type: 'variable', name: token.text, position: token.position };
        next();
        return { type: 'call', name: token.text, args: argumentsList(), position: token.position };
      case 'lparen': {
        const inner = expression(0);
        expect('rparen', '")"');
        return inner;
      }
      case 'operator':
        if (token.text === '-' || token.text === '+')
          return { type: 'unary', operator: token.text, operand: expression(UNARY_PRECEDENCE) };
    }
    throw new ExpressionError(`Unexpected ${describe(token)}`, token.position);
  }

  function argumentsList(): Node[] {
    const args: Node[] = [];
    if (peek().kind === 'rparen') {
      next();
      return args;
    }
    for (;;) {
      args.push(expression(0));
      const token = next();
      if (token.kind === 'rparen') return args;
      if (token.kind !== 'comma') throw new ExpressionError(`Expected "," or ")" but found ${describe(token)}`, token.position);
    }
  }

  const tree = expression(0);
  if (peek().kind !== 'end') throw new ExpressionError(`Unexpected ${describe(peek())}`, peek().position);
  return tree;
}

function describe(token: Token): string {
  return token.kind === 'end' ? 'end of input' : `"${token.text}"`;
}

/** Prints a tree with only the parentheses its precedence needs; parse(format(tree)) gives the same tree. */
export function format(node: Node): string {
  switch (node.type) {
    case 'number':
      return String(node.value);
    case 'variable':
      return node.name;
    case 'call':
      return `${node.name}(${node.args.map(format).join(', ')})`;
    case 'unary': {
      const operand = format(node.operand);
      return node.operand.type === 'binary' && BINARY[node.operand.operator]!.precedence < UNARY_PRECEDENCE
        ? `${node.operator}(${operand})`
        : node.operator + (node.operand.type === 'unary' ? ' ' : '') + operand;
    }
    case 'binary': {
      const { precedence, rightAssociative } = BINARY[node.operator]!;
      const side = (child: Node, isRight: boolean) => {
        const text = format(child);
        const childPrecedence =
          child.type === 'binary' ? BINARY[child.operator]!.precedence : child.type === 'unary' ? UNARY_PRECEDENCE : Infinity;
        const needsParens =
          childPrecedence < precedence ||
          (childPrecedence === precedence && (isRight !== rightAssociative)) ||
          (node.operator === '^' && !isRight && child.type === 'unary');
        return needsParens ? `(${text})` : text;
      };
      return `${side(node.left, false)} ${node.operator} ${side(node.right, true)}`;
    }
  }
}
