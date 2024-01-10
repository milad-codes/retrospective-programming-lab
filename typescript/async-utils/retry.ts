/** Retries a failing async operation with exponential backoff and full jitter. */

export interface RetryOptions {
  attempts: number; // total tries, including the first
  baseDelayMs: number;
  maxDelayMs: number;
  /** Return false for errors that retrying can't fix (e.g. validation errors). */
  shouldRetry?: (error: unknown) => boolean;
  /** Injected for tests; defaults to a real timer. */
  sleep?: (ms: number) => Promise<void>;
  random?: () => number;
}

/** Delay before retry n (1-based): a random value up to min(max, base · 2^(n-1)) — "full jitter". */
export const backoffDelay = (retry: number, options: Pick<RetryOptions, 'baseDelayMs' | 'maxDelayMs'>, random = Math.random) =>
  Math.floor(random() * Math.min(options.maxDelayMs, options.baseDelayMs * 2 ** (retry - 1)));

export async function retry<T>(operation: (attempt: number) => Promise<T>, options: RetryOptions): Promise<T> {
  const sleep = options.sleep ?? ((ms) => new Promise<void>((resolve) => setTimeout(resolve, ms)));
  for (let attempt = 1; ; attempt += 1) {
    try {
      return await operation(attempt);
    } catch (error) {
      const retryable = options.shouldRetry?.(error) ?? true;
      if (!retryable || attempt >= options.attempts) throw error;
      await sleep(backoffDelay(attempt, options, options.random));
    }
  }
}
