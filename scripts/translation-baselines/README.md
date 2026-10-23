# Translation source baselines

`sdk/concepts.md` preserves the English source at
`668f4beb2c6392f71202f4812793d12b70f826f3`, before the transport concepts rewrite.

The existing 17 translations still describe that earlier page. The verifier
compares them with this snapshot to retain code, link, and structure checks while
making the pending retranslation explicit. This snapshot is a verification
fixture, not current SDK API guidance: its reference to `transport.PacketConn`
is corrected to `net.Conn` in the rewritten English page.

When updating the translations, remove the baseline mapping and snapshot once
all locales reflect the new page.
