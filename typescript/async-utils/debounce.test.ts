import assert from 'node:assert/strict';
import { mock, test } from 'node:test';
import { debounce, throttle } from './debounce.ts';

test('debounce runs once with the last arguments after the calls stop', (t) => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  const calls: string[] = [];
  const save = debounce((text: string) => calls.push(text), 100);
  save('a');
  t.mock.timers.tick(50);
  save('ab');
  t.mock.timers.tick(99);
  assert.deepEqual(calls, []);
  t.mock.timers.tick(1);
  assert.deepEqual(calls, ['ab']);
});

test('debounce can be cancelled or flushed', (t) => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  const fn = mock.fn();
  const debounced = debounce(fn, 100);
  debounced(1);
  debounced.cancel();
  t.mock.timers.tick(200);
  assert.equal(fn.mock.callCount(), 0);
  debounced(2);
  debounced.flush();
  assert.deepEqual(fn.mock.calls.map((c) => c.arguments), [[2]]);
});

test('throttle runs the first call at once and the last call of a burst at the end of the interval', (t) => {
  t.mock.timers.enable({ apis: ['setTimeout', 'Date'] });
  const calls: number[] = [];
  const onScroll = throttle((y: number) => calls.push(y), 100);
  for (let y = 1; y <= 5; y += 1) {
    onScroll(y);
    t.mock.timers.tick(10);
  }
  assert.deepEqual(calls, [1]);
  t.mock.timers.tick(60);
  assert.deepEqual(calls, [1, 5]);
  t.mock.timers.tick(200);
  onScroll(6);
  assert.deepEqual(calls, [1, 5, 6]);
});
