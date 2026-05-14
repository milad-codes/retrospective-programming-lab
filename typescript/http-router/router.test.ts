import assert from 'node:assert/strict';
import { test } from 'node:test';
import { Router } from './router.ts';

const request = (method: string, path: string) => ({ method, path, query: new URLSearchParams(), body: undefined, headers: {} });

test('matches static and parameter segments, decoding parameters', async () => {
  const router = new Router()
    .get('/users', () => ({ status: 200, body: 'list' }))
    .get('/users/:id', (r) => ({ status: 200, body: r.params }))
    .get('/users/:id/posts/:post', (r) => ({ status: 200, body: r.params }));
  assert.deepEqual((await router.handle(request('GET', '/users/'))).body, 'list');
  assert.deepEqual((await router.handle(request('GET', '/users/a%20b'))).body, { id: 'a b' });
  assert.deepEqual((await router.handle(request('GET', '/users/7/posts/9'))).body, { id: '7', post: '9' });
});

test('distinguishes 404 from 405 and lists allowed methods', async () => {
  const router = new Router().get('/items', () => ({ status: 200 })).post('/items', () => ({ status: 201 }));
  assert.equal((await router.handle(request('GET', '/nothing'))).status, 404);
  const response = await router.handle(request('DELETE', '/items'));
  assert.equal(response.status, 405);
  assert.equal(response.headers?.allow, 'GET, HEAD, POST');
});

test('answers HEAD with the GET route and no body', async () => {
  const router = new Router().get('/ping', () => ({ status: 200, body: 'pong' }));
  assert.deepEqual(await router.handle(request('HEAD', '/ping')), { status: 200, body: undefined });
});

test('runs middleware around the handler in order', async () => {
  const log: string[] = [];
  const router = new Router()
    .use(async (_r, next) => {
      log.push('outer in');
      const response = await next();
      log.push('outer out');
      return { ...response, headers: { 'x-trace': 'yes' } };
    })
    .use(async (_r, next) => {
      log.push('inner');
      return next();
    })
    .get('/', () => {
      log.push('handler');
      return { status: 204 };
    });
  const response = await router.handle(request('GET', '/'));
  assert.deepEqual(log, ['outer in', 'inner', 'handler', 'outer out']);
  assert.equal(response.headers?.['x-trace'], 'yes');
});

test('rejects malformed percent-encoding and duplicate parameter names', async () => {
  const router = new Router().get('/files/:name', () => ({ status: 200 }));
  assert.equal((await router.handle(request('GET', '/files/%E0%A4%A'))).status, 404);
  assert.throws(() => new Router().get('/a/:id/:id', () => ({ status: 200 })), /duplicate/);
});
