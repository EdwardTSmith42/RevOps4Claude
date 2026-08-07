# `.gitignore` defaults for Personal OS

The `.gitignore` the setup wizard generates. Excludes are organized by category with a one-line rationale.

The user can extend or remove entries; the wizard surfaces the defaults during setup and confirms before writing.

## Secrets

```
# Environment files
.env
.env.local
.env.*.local

# Keys and credentials
*.key
*.pem
id_rsa
id_ed25519
*.p12
*.pfx

# API tokens
.token
*-token.txt
api-keys.json

# Sensitive config
config/secrets.yml
config/credentials.yml.enc
```

**Rationale:** Anything that looks like a credential never enters version control. The wizard scans for these patterns during setup; if any matched files exist already, surface them and confirm exclusion.

## Operating-system junk

```
# macOS
.DS_Store
._*
.Spotlight-V100
.Trashes

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# Linux
.directory
```

**Rationale:** Junk files that don't represent actual workspace state. Excluding keeps commits clean.

## Sensitive Personal OS inputs

```
# Email account profiles (contain user-specific filter lists, sender data)
os-inputs/email-accounts/

# Setup philosophy (contains user's personal governance preferences; private by default — confirm during setup)
os-inputs/_os-setup-philosophy.md
```

**Rationale:** Per the workspace's "skills ship empty templates; user data populates at runtime" principle — these files are user-generated and contain personal filter lists, sender data, or governance preferences. Default exclude protects privacy. The wizard asks the user to confirm; users who want to back up their preferences can opt in.

## Cache and temp directories

```
# Generic
.cache/
*.tmp
*.bak
*~

# Python (if any user skill uses Python)
__pycache__/
*.pyc
*.pyo

# Node (if any user skill uses Node)
node_modules/
.npm/

# Editor swap files
.swp
.swo
```

**Rationale:** Build artifacts and cache files don't belong in version control. They regenerate locally.

## Cowork session artifacts

```
# Session output directories
sessions/
.cowork/
```

**Rationale:** Session-specific artifacts that don't represent workspace state.

## Logs

```
*.log
logs/
```

**Rationale:** Logs are noisy and regenerate. If a specific log matters, the user can override.

## What's NOT excluded by default

These are intentionally tracked:

- `skills/` — all skills
- `os-inputs/` (except the sensitive subdirs above) — voiceprints, briefs, templates, the user's profile, the inbox
- `os-knowledge/` — durable concepts and frameworks

## Customization

The user can extend the `.gitignore` directly (it's a normal file at the workspace root). The wizard offers to surface common additions during setup — asking whether there are specific folders or file types the user wants to keep local-only. Anything added beyond the defaults is preserved across re-runs of the wizard.
