# Async utilities

Small, dependency-free versions of helpers every JavaScript codebase ends up needing.

| File | Function | Behaviour worth knowing |
| --- | --- | --- |
| `pool.ts` | `mapWithLimit(items, limit, task)` | at most `limit` tasks at once; results in input order; after the first failure no new tasks start |
| `retry.ts` | `retry(operation, options)` | exponential backoff with full jitter, a delay cap, and `shouldRetry` for errors retrying can't fix |
| `debounce.ts` | `debounce`, `throttle` | debounce has `cancel` and `flush`; throttle runs the first call and the last one of a burst |

The tests use `node:test`'s mock timers or injected `sleep` and `random` functions, so they check exact timings without
waiting in real time.

```bash
node --test typescript/async-utils/
```
