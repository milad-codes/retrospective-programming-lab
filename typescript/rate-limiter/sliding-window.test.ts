import assert from 'node:assert/strict';
import { test } from 'node:test';
import { SlidingWindowLimiter } from './sliding-window.ts';

test('allows at most the limit in any window, per key', () => {
  let now = 0;
  const limiter = new SlidingWindowLimiter(2, 1000, () => now);
  assert.equal(limiter.tryAcquire('a').allowed, true);
  now = 400;
  assert.equal(limiter.tryAcquire('a').allowed, true);
  now = 900;
  assert.deepEqual(limiter.tryAcquire('a'), { allowed: false, retryAfterMs: 100 });
  assert.equal(limiter.tryAcquire('b').allowed, true);
  now = 1000;
  assert.equal(limiter.tryAcquire('a').allowed, true); // the event at 0 has left the window
});

test('never exceeds the limit in any window under random traffic', () => {
  let now = 0;
  let seed = 3;
  const random = () => ((seed = (seed * 16_807) % 2_147_483_647) / 2_147_483_647);
  const limiter = new SlidingWindowLimiter(5, 1000, () => now);
  const allowed: number[] = [];
  for (let i = 0; i < 5000; i += 1) {
    now += Math.floor(random() * 120);
    if (limiter.tryAcquire('client').allowed) allowed.push(now);
  }
  for (let i = 0; i + 5 < allowed.length; i += 1) assert.ok(allowed[i + 5]! - allowed[i]! >= 1000);
});

test('prunes idle keys', () => {
  let now = 0;
  const limiter = new SlidingWindowLimiter(1, 100, () => now);
  limiter.tryAcquire('a');
  limiter.tryAcquire('b');
  now = 150;
  limiter.tryAcquire('b');
  limiter.prune();
  assert.equal(limiter.trackedKeys, 1);
});
