# Translation source baselines

`sdk/command-line-debugging.md` preserves the English source at
`668f4beb2c6392f71202f4812793d12b70f826f3`, before the CLI guide was split into Fetch,
DNS Lookups, Local HTTP Proxy, and Remote Measurement.

The existing 17 translations still describe that combined guide. The verifier
compares them with this snapshot to retain code, link, and structure checks while
making the pending retranslation explicit. The three new guides fall back to
English through Docusaurus and are listed in `ENGLISH_ONLY`. Their links to Fetch
use its canonical English URL because the translated guide does not yet have
the new ECH and transport sections.

When updating the translated guide to the new structure, remove its baseline
mapping and snapshot once all locales are updated. Remove each new guide from
`ENGLISH_ONLY` when its translations are available.
