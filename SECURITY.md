# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub's
[security advisory form](https://github.com/mthomason/mbot/security/advisories/new)
rather than opening a public issue.

## Automated checks

CI runs on every push and pull request:

- `npm audit --omit=dev --audit-level=high` for shipped frontend dependencies
- `pip-audit -r requirements.txt` for backend dependencies
- `bundler-audit check` for the docs site
- Dependabot updates for npm, pip, RubyGems, and GitHub Actions

## Known dev-only advisory

`picomatch` [GHSA-fc5q-39xc-vjpf](https://github.com/advisories/GHSA-fc5q-39xc-vjpf)
(ReDoS) affects versions `<= 4.0.7` and currently has **no patched release**.
It is pulled in only by build/test tooling (`vite`, `vitest`, `svelte-check`,
`tinyglobby`, and the ESLint toolchain) and is not part of the production
bundle. All remaining `npm audit` findings are this single transitive advisory.
The blocking CI audit therefore covers production dependencies only;
Dependabot will alert when a patched release is available.
