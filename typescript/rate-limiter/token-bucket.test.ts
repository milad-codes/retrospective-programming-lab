import assert from 'node:assert/strict';
import { test } from 'node:test';
import { TokenBucket } from './token-bucket.ts';

test('allows a burst up to the capacity, then the refill rate', () => {
  let now = 0;
  const bucket = new TokenBucket(3, 2, () => now); // 3 tokens, 2 per second
  assert.deepEqual([1, 2, 3, 4].map(() => bucket.tryTake()), [true, true, true, false]);
  assert.equal(bucket.waitTimeMs(), 500);
  now = 499;
  assert.equal(bucket.tryTake(), false);
  now = 500;
  assert.equal(bucket.tryTake(), true);
});

test('never stores more than the capacity', () => {
  let now = 0;
  const bucket = new TokenBucket(2, 10, () => now);
  now = 60_000;
  assert.deepEqual([1, 2, 3].map(() => bucket.tryTake()), [true, true, false]);
});

test('long-run throughput equals the refill rate', () => {
  let now = 0;
  const bucket = new TokenBucket(5, 4, () => now);
  let allowed = 0;
  for (now = 0; now <= 10_000; now += 10) if (bucket.tryTake()) allowed += 1;
  assert.equal(allowed, 5 + 40); // the initial burst plus 4 per second for 10 seconds
});

test('validates its configuration and costs', () => {
  assert.throws(() => new TokenBucket(0, 1), RangeError);
  const bucket = new TokenBucket(5, 1, () => 0);
  assert.equal(bucket.tryTake(6), false);
  assert.equal(bucket.tryTake(5), true);
});
