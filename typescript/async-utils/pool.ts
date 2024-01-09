/** Runs async tasks with a concurrency limit and returns results in input order, like Promise.all. */

export async function mapWithLimit<T, R>(
  items: readonly T[],
  limit: number,
  task: (item: T, index: number) => Promise<R>,
): Promise<R[]> {
  if (!Number.isInteger(limit) || limit < 1) throw new RangeError('limit must be a positive integer');
  const results = new Array<R>(items.length);
  let next = 0;
  let failed = false;

  // each worker takes the next index until none are left; JavaScript's single thread makes `next++` safe
  async function worker(): Promise<void> {
    while (!failed && next < items.length) {
      const index = next++;
      try {
        results[index] = await task(items[index]!, index);
      } catch (error) {
        failed = true; // stop starting new tasks; tasks already running finish on their own
        throw error;
      }
    }
  }

  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return results;
}
