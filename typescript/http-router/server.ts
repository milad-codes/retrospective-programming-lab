/** Connects the Router to node:http: JSON bodies in and out, errors become 400 or 500 responses. */
import { createServer, type IncomingMessage, type Server } from 'node:http';
import type { Router } from './router.ts';

const MAX_BODY_BYTES = 64 * 1024;

export class BadRequest extends Error {}

async function readJson(request: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  let size = 0;
  for await (const chunk of request) {
    size += (chunk as Buffer).length;
    if (size > MAX_BODY_BYTES) throw new BadRequest('body too large');
    chunks.push(chunk as Buffer);
  }
  if (size === 0) return undefined;
  if (!request.headers['content-type']?.startsWith('application/json')) throw new BadRequest('expected application/json');
  try {
    return JSON.parse(Buffer.concat(chunks).toString('utf8'));
  } catch {
    throw new BadRequest('invalid JSON');
  }
}

export function serve(router: Router): Server {
  return createServer(async (req, res) => {
    let status = 500;
    let headers: Record<string, string> = {};
    let body: unknown = { error: 'Internal server error' };
    try {
      const url = new URL(req.url ?? '/', 'http://localhost');
      const response = await router.handle({
        method: req.method ?? 'GET',
        path: url.pathname,
        query: url.searchParams,
        body: await readJson(req),
        headers: req.headers as Record<string, string | undefined>,
      });
      ({ status, headers = {}, body } = response);
    } catch (error) {
      if (error instanceof BadRequest) {
        status = 400;
        body = { error: error.message };
      }
    }
    const payload = body === undefined ? '' : JSON.stringify(body);
    res.writeHead(status, {
      ...headers,
      ...(payload ? { 'content-type': 'application/json' } : {}),
      'content-length': Buffer.byteLength(payload),
    });
    res.end(payload);
  });
}
