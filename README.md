# Technical Writer

A protoAgent archetype that writes and maintains documentation for a codebase.
It turns source evidence into guides, tutorials, reference, and explanations, and
owns systematic audits, reader paths, media planning, and verified delivery.

## Set up

Use a protoAgent build containing the `technical_writer` bundled plugin and
`technical-writer` soul preset. This is a new core addition, not available in
older releases merely because they support archetypes. Core introduction is tracked in
[protoAgent PR #4338](https://github.com/protoLabsAI/protoAgent/pull/4338); use a checkout
containing that implementation until a release includes it.

Choose **Technical Writer** in the new-agent picker. Supply a local checkout in
**Local codebase**, or leave it blank and give the agent a GitHub repository from
chat. An existing compatible host can also install the bundle:

```sh
protoagent plugin install https://github.com/protoLabsAI/technical-writer-archetype
```

The bundle enables the built-in skill pack and suggests project filesystem and
onboarding settings. Clones default to `~/code`, with GitHub sources allowed;
narrow those settings for your environment. Reads and edits remain project-fenced.
Commands require approval except the listed read-only Git commands. Repository
build tools must be installed separately. A configured model connection is required.
No GitHub account, browser/capture tool, or deployment credential is provisioned.
For PR delivery, supply an authenticated CLI or connector and authorize shipping.

## Give it a job

- “Write a tutorial from installation to the first successful result in this repo.”
- “Audit every operator guide for stale commands, redundancy, and missing recovery
  steps. Record prioritized tasks before implementing changes.”
- “Execute the approved task list section by section, validate, and ship reviewed PRs.”
- “Review the navigation for app users, builders, and operators; preserve old links.”
- “Audit visual needs and add reusable media slots with capture briefs and refresh tracking.”

The persona loads six skills as needed: `docs-discover`, `docs-write`, `docs-audit`,
`docs-structure`, `docs-media`, and `docs-verify`. Their canonical source and behavioral
review scenarios live in the [core skill pack](https://github.com/protoLabsAI/protoAgent/tree/main/plugins/technical_writer).
The [persona](https://github.com/protoLabsAI/protoAgent/blob/main/config/soul-presets/technical-writer.md)
also lives in core; this repository only composes the install.

Audit-only work stays read-only. Authorized implementation continues without repeated
approval requests. Publishing and merging still require authorization and the target
repository's gates. Reports distinguish source checks, executed examples, previews,
CI, and deployment. A media registry is not a finished set of screenshots or videos.

## Verify

From a compatible protoAgent checkout with dependencies synced:

```sh
uv run --no-sync python /path/to/technical-writer-archetype/scripts/verify_bundle.py /path/to/technical-writer-archetype
```

The bundle directory must be committed in a Git repository. The verifier installs it
into temporary box/instance roots, loads the plugin and skills, checks the persona,
and checks core tool binding. It does not test model writing quality, native UI,
remote publishing, or real capture/playback. CI repeats this against core `main`;
all members are built-in, so there are no external release pins to update.
