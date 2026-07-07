# Privacy Policy

**Last updated:** 7 July 2026

Claude Compass is a free, open-source plugin for Anthropic's Claude Cowork. This policy explains what data is involved when you use it and what rights you have.

---

## What data does Claude Compass touch?

Claude Compass processes the following data during a session:

- **Resume content** — you upload or paste your resume. Claude extracts structured information from it and saves it as `profile.md` in your Cowork workspace.
- **Situational information** — your current location, citizenship, languages, and any known immigration friction. Saved as `situational-profile.md` in your workspace.
- **Job criteria** — salary minimums, timezone preferences, relocation openness, and dealbreakers you provide during a session. Held in memory during the session and referenced in state files.
- **Research data** — salary and visa research you paste in. Saved to research files in your workspace.
- **Session state** — pipeline progress is saved to `.country-finder-state.json` and `.salary-calculator-state.json` so sessions can resume if interrupted.

All of these files are written to **your own Cowork workspace only**. Claude Compass does not transmit, upload, or store any of this data on external servers. The developer of Claude Compass has no access to it.

---

## Does Claude Compass collect any data about me?

No. Claude Compass is a markdown-only plugin with no server, no database, no telemetry, and no analytics. The developer (Myo Win Thein) receives no data from your use of the plugin.

---

## What about Anthropic and Claude?

Claude Compass runs inside Anthropic's Claude Cowork environment. When you use Claude Compass, your messages and the content you paste are processed by Claude (Anthropic's AI). Anthropic's own privacy policy governs how they handle that data. You can review it at [anthropic.com/privacy](https://www.anthropic.com/privacy).

---

## Third-party services on the documentation site

The Claude Compass documentation site (hosted on GitHub Pages at `myowinthein.github.io/claude-compass`) loads the following third-party resources:

- **jsDelivr CDN** (`cdn.jsdelivr.net`) — used to load the Mermaid diagram library. jsDelivr may log your IP address as part of normal CDN operation.
- **myowin.dev** — used to serve the site's favicon. This domain may log your IP address.

These third-party services operate under their own privacy policies. No tracking or analytics cookies are set by the documentation site.

---

## Your rights under GDPR

If you are located in the European Economic Area, you have the following rights regarding any personal data that concerns you:

- **Access** — request a copy of the data held about you
- **Rectification** — request correction of inaccurate data
- **Erasure** — request deletion of your data
- **Portability** — request your data in a portable format
- **Objection** — object to processing of your data

Because Claude Compass holds no data on its own servers, these rights apply primarily to data held by Anthropic (governed by their policy) and the CDN providers listed above.

---

## Data retention

All data Claude Compass creates (profile.md, state files, research files) lives in your Cowork workspace and is retained until you delete it. The developer retains no data.

---

## Contact

For questions about this policy, open an issue at [github.com/myowinthein/claude-compass/issues](https://github.com/myowinthein/claude-compass/issues).
