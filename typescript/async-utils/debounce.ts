/** Debounce: run once after calls have stopped for `waitMs`. Throttle: run at most once per `intervalMs`. */

export interface Debounced<A extends unknown[]> {
  (...args: A): void;
  cancel(): void;
  flush(): void;
}

export function debounce<A extends unknown[]>(fn: (...args: A) => void, waitMs: number): Debounced<A> {
  let timer: ReturnType<typeof setTimeout> | undefined;
  let lastArgs: A | undefined;
  const run = () => {
    timer = undefined;
    const args = lastArgs!;
    lastArgs = undefined;
    fn(...args);
  };
  const debounced = (...args: A) => {
    lastArgs = args;
    clearTimeout(timer);
    timer = setTimeout(run, waitMs);
  };
  debounced.cancel = () => {
    clearTimeout(timer);
    timer = undefined;
    lastArgs = undefined;
  };
  debounced.flush = () => {
    if (timer !== undefined) {
      clearTimeout(timer);
      run();
    }
  };
  return debounced;
}

/** Leading and trailing: the first call runs at once, the last call of a burst runs when the interval ends. */
export function throttle<A extends unknown[]>(fn: (...args: A) => void, intervalMs: number): (...args: A) => void {
  let last = -Infinity;
  let pending: A | undefined;
  let timer: ReturnType<typeof setTimeout> | undefined;
  const fire = (args: A) => {
    last = Date.now();
    fn(...args);
  };
  return (...args: A) => {
    const wait = last + intervalMs - Date.now();
    if (wait <= 0 && timer === undefined) {
      fire(args);
      return;
    }
    pending = args;
    timer ??= setTimeout(() => {
      timer = undefined;
      const latest = pending!;
      pending = undefined;
      fire(latest);
    }, Math.max(wait, 0));
  };
}
