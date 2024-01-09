import assert from 'node:assert/strict';
import { test } from 'node:test';
import { setTimeout as sleep } from 'node:timers/promises';
import { mapWithLimit } from './pool.ts';

test('keeps input order and never exceeds the limit', async () => {
  let running = 0;
  let peak = 0;
  const results = await mapWithLimit([30, 10, 20, 5, 15, 25], 2, async (ms, index) => {
    running += 1;
    peak = Math.max(peak, running);
    await sleep(ms);
    running -= 1;
    return index * 10;
  });
  assert.deepEqual(results, [0, 10, 20, 30, 40, 50]);
  assert.equal(peak, 2);
});

test('stops starting tasks after a failure and rejects with it', async () => {
  const started: number[] = [];
  await assert.rejects(
    mapWithLimit([1, 2, 3, 4, 5, 6], 2, async (n) => {
      started.push(n);
      await sleep(5);
      if (n === 2) throw new Error('task 2 failed');
      return n;
    }),
    /task 2 failed/,
  );
  assert.ok(started.length < 6, `started ${started.join(',')}`);
});

test('handles empty input and rejects bad limits', async () => {
  assert.deepEqual(await mapWithLimit([], 3, async () => 1), []);
  await assert.rejects(mapWithLimit([1], 0, async () => 1), RangeError);
});
