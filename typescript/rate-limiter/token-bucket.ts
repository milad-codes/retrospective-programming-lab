/**
 * Token bucket: holds up to `capacity` tokens and refills at `refillPerSecond`. A request takes one token, so short
 * bursts up to the capacity are allowed while the long-run rate stays at the refill rate.
 */
export class TokenBucket {
  readonly capacity: number;
  readonly refillPerSecond: number;
  private readonly now: () => number;
  private tokens: number;
  private updatedAt: number;

  constructor(capacity: number, refillPerSecond: number, now: () => number = Date.now) {
    if (capacity <= 0 || refillPerSecond <= 0) throw new RangeError('capacity and refill rate must be positive');
    this.capacity = capacity;
    this.refillPerSecond = refillPerSecond;
    this.now = now;
    this.tokens = capacity;
    this.updatedAt = now();
  }

  /** Takes `cost` tokens if available. Returns false (and takes nothing) otherwise. */
  tryTake(cost = 1): boolean {
    this.refill();
    if (this.tokens < cost) return false;
    this.tokens -= cost;
    return true;
  }

  /** Milliseconds until `cost` tokens will be available; 0 if they are now. Useful for a Retry-After header. */
  waitTimeMs(cost = 1): number {
    this.refill();
    return this.tokens >= cost ? 0 : Math.ceil(((cost - this.tokens) / this.refillPerSecond) * 1000);
  }

  private refill(): void {
    const now = this.now();
    // tokens accumulate lazily from elapsed time; no timers involved
    this.tokens = Math.min(this.capacity, this.tokens + ((now - this.updatedAt) / 1000) * this.refillPerSecond);
    this.updatedAt = now;
  }
}
