import assert from 'node:assert/strict';
import type { AddressInfo } from 'node:net';
import { after, before, test } from 'node:test';
import { Router } from './router.ts';
import { serve } from './server.ts';

const notes = new Map<string, string>();
const router = new Router()
  .post('/notes/:id', (r) => {
    const text = (r.body as { text?: unknown } | undefined)?.text;
    if (typeof text !== 'string') return { status: 422, body: { error: 'text must be a string' } };
    notes.set(r.params.id!, text);
    return { status: 201, body: { id: r.params.id, text } };
  })
  .get('/notes/:id', (r) =>
    notes.has(r.params.id!) ? { status: 200, body: { text: notes.get(r.params.id!) } } : { status: 404, body: { error: 'no such note' } },
  )
  .get('/boom', () => {
    throw new Error('handler crashed');
  });
const server = serve(router);
let base = '';

before(async () => {
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
after(() => server.close());

test('round-trips JSON over real HTTP', async () => {
  const created = await fetch(`${base}/notes/n1`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ text: 'hello' }),
  });
  assert.equal(created.status, 201);
  assert.deepEqual(await (await fetch(`${base}/notes/n1`)).json(), { text: 'hello' });
});

test('maps bad input to 400 and crashes to 500 without leaking the message', async () => {
  const bad = await fetch(`${base}/notes/n2`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{oops' });
  assert.equal(bad.status, 400);
  const crash = await fetch(`${base}/boom`);
  assert.equal(crash.status, 500);
  assert.deepEqual(await crash.json(), { error: 'Internal server error' });
  const wrongMethod = await fetch(`${base}/notes/n1`, { method: 'DELETE' });
  assert.equal(wrongMethod.status, 405);
  assert.equal(wrongMethod.headers.get('allow'), 'GET, HEAD, POST');
});
