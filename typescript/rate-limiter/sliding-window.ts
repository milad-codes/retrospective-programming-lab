/**
 * Sliding-window log: allows at most `limit` events in any `windowMs` interval. Exact, at the cost of storing one
 * timestamp per allowed event and key. Keys are independent (e.g. one per client).
 */
export class SlidingWindowLimiter {
  readonly limit: number;
  readonly windowMs: number;
  private readonly now: () => number;
  private readonly events = new Map<string, number[]>();

  constructor(limit: number, windowMs: number, now: () => number = Date.now) {
    if (limit < 1 || windowMs <= 0) throw new RangeError('limit and window must be positive');
    this.limit = limit;
    this.windowMs = windowMs;
    this.now = now;
  }

  tryAcquire(key: string): { allowed: boolean; retryAfterMs: number } {
    const now = this.now();
    const log = (this.events.get(key) ?? []).filter((t) => t > now - this.windowMs);
    if (log.length < this.limit) {
      log.push(now);
      this.events.set(key, log);
      return { allowed: true, retryAfterMs: 0 };
    }
    this.events.set(key, log);
    return { allowed: false, retryAfterMs: log[0]! + this.windowMs - now };
  }

  /** Drops keys with no events in the current window, so idle clients don't keep memory forever. */
  prune(): void {
    const cutoff = this.now() - this.windowMs;
    for (const [key, log] of this.events) if (log.every((t) => t <= cutoff)) this.events.delete(key);
  }

  get trackedKeys(): number {
    return this.events.size;
  }
}
