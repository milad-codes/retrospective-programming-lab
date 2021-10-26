/** Evaluates a parsed expression with variables and a small set of functions. */
import { ExpressionError } from './lexer.ts';
import { type Node, parse } from './parser.ts';

type Fn = { arity: [number, number]; apply: (...args: number[]) => number };

const FUNCTIONS: Record<string, Fn> = {
  abs: { arity: [1, 1], apply: Math.abs },
  sqrt: { arity: [1, 1], apply: Math.sqrt },
  min: { arity: [1, Infinity], apply: Math.min },
  max: { arity: [1, Infinity], apply: Math.max },
  round: {
    arity: [1, 2],
    apply: (value, digits = 0) => {
      const factor = 10 ** digits;
      return Math.round(value * factor) / factor;
    },
  },
};

export function evaluate(node: Node, variables: Readonly<Record<string, number>> = {}): number {
  switch (node.type) {
    case 'number':
      return node.value;
    case 'variable': {
      const value = variables[node.name];
      if (value === undefined) throw new ExpressionError(`Unknown variable "${node.name}"`, node.position);
      return value;
    }
    case 'unary': {
      const value = evaluate(node.operand, variables);
      return node.operator === '-' ? -value : value;
    }
    case 'binary': {
      const left = evaluate(node.left, variables);
      const right = evaluate(node.right, variables);
      switch (node.operator) {
        case '+':
          return left + right;
        case '-':
          return left - right;
        case '*':
          return left * right;
        case '/':
        case '%':
          if (right === 0) throw new ExpressionError('Division by zero', 0);
          return node.operator === '/' ? left / right : left % right;
        default:
          return left ** right;
      }
    }
    case 'call': {
      const fn = FUNCTIONS[node.name];
      if (!fn) throw new ExpressionError(`Unknown function "${node.name}"`, node.position);
      const [min, max] = fn.arity;
      if (node.args.length < min || node.args.length > max) {
        const expected = min === max ? `${min}` : max === Infinity ? `at least ${min}` : `${min} to ${max}`;
        throw new ExpressionError(`${node.name}() takes ${expected} argument(s), got ${node.args.length}`, node.position);
      }
      return fn.apply(...node.args.map((arg) => evaluate(arg, variables)));
    }
  }
}

/** Parses and evaluates in one step: calculate('2 * (x + 1)', { x: 4 }) === 10. */
export const calculate = (source: string, variables: Readonly<Record<string, number>> = {}): number =>
  evaluate(parse(source), variables);
