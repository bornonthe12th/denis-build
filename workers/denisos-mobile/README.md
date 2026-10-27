# DenisOS phone home (mobile)

This folder records the Cloudflare Worker currently serving `denis.zone`.

## Behaviour

- **Desktop (>700px):** the existing DenisOS V3 experience is unchanged.
- **Mobile (<=700px):** after the existing unlock screen, show a native-feeling phone home with nine app shortcuts and four dock favourites. Existing DenisOS apps open full-screen, and the Home button returns to the app grid.
- No independent copy of the V3 app is bundled: this Worker uses a **Cloudflare service binding** to the original V3 Worker.

## Cloudflare deployment

Deployed script: `denis-portfolio-v3-mobile-preview` (historical name; now serving production).

Custom domain: `denis.zone`.

Service binding **required**:
```json
{"type":"service","name":"UPSTREAM","service":"denis-portfolio-v3-preview","environment":"production"}
```

The binding is essential. The code calls `UPSTREAM.fetch()` to avoid recursion when the public custom domain points at the mobile wrapper. Do not deploy this source as a raw JS Worker without preserving that binding. Cloudflare multipart Worker upload metadata must include `body_part: "worker.js"` and the service binding above.

The original `denis-portfolio-v3-preview` Worker remains available for rollback; do not delete it. The original source for that V3 Worker is not part of this folder.

## Testing

Cloudflare browser rendering tests passed on 390x844 (five core apps) and 360x800 (all nine apps): full-screen app opening, Home navigation, viewport-width window sizing and no page-level horizontal overflow. Normal unlock was also tested. A desktop browser smoke test confirmed the underlying V3 interface still works.

## Rollback

Reassign the `denis.zone` Worker custom domain to `denis-portfolio-v3-preview`, leaving the phone wrapper Worker deployed for further iteration.

## Follow-up

Incorporate this mobile implementation into the main V3 app source when its repository is identified; the current wrapper is a separate Worker and not a rewrite of the original V3 application.
