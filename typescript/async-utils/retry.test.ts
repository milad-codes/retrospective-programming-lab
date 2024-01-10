import assert from 'node:assert/strict';
import { test } from 'node:test';
import { backoffDelay, retry } from './retry.ts';

const options = { attempts: 4, baseDelayMs: 100, maxDelayMs: 1000 };

test('retries until the operation succeeds, with growing delays', async () => {
  const delays: number[] = [];
  const result = await retry(
    async (attempt) => {
      if (attempt < 3) throw new Error(`fail ${attempt}`);
      return 'ok';
    },
    { ...options, sleep: async (ms) => void delays.push(ms), random: () => 0.999 },
  );
  assert.equal(result, 'ok');
  assert.deepEqual(delays, [99, 199]);
});

test('gives up after the last attempt with the last error', async () => {
  let calls = 0;
  await assert.rejects(
    retry(async () => {
      calls += 1;
      throw new Error(`fail ${calls}`);
    }, { ...options, sleep: async () => {} }),
    /fail 4/,
  );
  assert.equal(calls, 4);
});

test('does not retry errors the caller marks as permanent', async () => {
  let calls = 0;
  await assert.rejects(
    retry(async () => {
      calls += 1;
      throw new TypeError('bad input');
    }, { ...options, sleep: async () => {}, shouldRetry: (error) => !(error instanceof TypeError) }),
  );
  assert.equal(calls, 1);
});

test('caps the delay', () => {
  assert.equal(backoffDelay(10, options, () => 0.5), 500);
  assert.equal(backoffDelay(1, options, () => 0), 0);
});
