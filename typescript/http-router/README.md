# HTTP router

A router small enough to read in one sitting, plus an adapter for `node:http`.

- **Routing** (`router.ts`): static segments and `:param` captures (percent-decoded). A path with no matching route is
  a `404`. A path that exists without the requested method is a `405` with an `Allow` header. `HEAD` is served by the
  `GET` route without a body.
- **Middleware**: each one receives `next()` and can act before and after the handler (logging, headers, auth).
- **Server** (`server.ts`): reads JSON bodies up to 64 KB and answers `400` for bad JSON or the wrong content type.
  It answers `500` without exposing the error message when a handler throws.

`router.test.ts` tests the router without a network. `server.test.ts` starts a real server on a free port and talks to
it with `fetch`.

```bash
node --test typescript/http-router/
```
