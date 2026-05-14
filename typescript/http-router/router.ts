/**
 * A small HTTP router: path parameters (`/users/:id`), method matching, 404 vs 405 with an `Allow` header, and
 * middleware that runs around the handler. Framework-independent: it works on plain request and response objects.
 */

export interface RouteRequest {
  method: string;
  path: string;
  params: Record<string, string>;
  query: URLSearchParams;
  body: unknown;
  headers: Record<string, string | undefined>;
}

export interface RouteResponse {
  status: number;
  headers?: Record<string, string>;
  body?: unknown;
}

export type Handler = (request: RouteRequest) => RouteResponse | Promise<RouteResponse>;
export type Middleware = (request: RouteRequest, next: () => Promise<RouteResponse>) => Promise<RouteResponse>;

interface Route {
  method: string;
  segments: string[];
  handler: Handler;
}

const splitPath = (path: string): string[] => path.split('/').filter(Boolean);

export class Router {
  private readonly routes: Route[] = [];
  private readonly middleware: Middleware[] = [];

  use(middleware: Middleware): this {
    this.middleware.push(middleware);
    return this;
  }

  on(method: string, pattern: string, handler: Handler): this {
    const segments = splitPath(pattern);
    const names = segments.filter((s) => s.startsWith(':'));
    if (new Set(names).size !== names.length) throw new Error(`duplicate parameter name in ${pattern}`);
    this.routes.push({ method: method.toUpperCase(), segments, handler });
    return this;
  }

  get(pattern: string, handler: Handler): this {
    return this.on('GET', pattern, handler);
  }

  post(pattern: string, handler: Handler): this {
    return this.on('POST', pattern, handler);
  }

  async handle(request: Omit<RouteRequest, 'params'>): Promise<RouteResponse> {
    const path = splitPath(request.path);
    const allowed = new Set<string>();
    let found: { route: Route; params: Record<string, string> } | undefined;
    for (const route of this.routes) {
      const params = match(route.segments, path);
      if (!params) continue;
      allowed.add(route.method);
      // HEAD is answered by GET routes without a body
      if (!found && (route.method === request.method || (request.method === 'HEAD' && route.method === 'GET'))) {
        found = { route, params };
      }
    }
    if (!found) {
      if (allowed.size === 0) return { status: 404, body: { error: 'Not found' } };
      if (allowed.has('GET')) allowed.add('HEAD');
      return { status: 405, headers: { allow: [...allowed].sort().join(', ') }, body: { error: 'Method not allowed' } };
    }
    const full: RouteRequest = { ...request, params: found.params };
    const run = (i: number): Promise<RouteResponse> =>
      i < this.middleware.length
        ? this.middleware[i]!(full, () => run(i + 1))
        : Promise.resolve(found.route.handler(full));
    const response = await run(0);
    return request.method === 'HEAD' ? { ...response, body: undefined } : response;
  }
}

/** Static segments must match exactly; `:name` captures one decoded segment. */
function match(pattern: string[], path: string[]): Record<string, string> | undefined {
  if (pattern.length !== path.length) return undefined;
  const params: Record<string, string> = {};
  for (let i = 0; i < pattern.length; i += 1) {
    const expected = pattern[i]!;
    const actual = path[i]!;
    if (expected.startsWith(':')) {
      try {
        params[expected.slice(1)] = decodeURIComponent(actual);
      } catch {
        return undefined; // malformed percent-encoding never matches
      }
    } else if (expected !== actual) {
      return undefined;
    }
  }
  return params;
}
