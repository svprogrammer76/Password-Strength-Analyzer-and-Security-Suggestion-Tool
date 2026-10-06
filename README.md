# Password Strength Analyzer & Security Suggestion Tool

Privacy-focused defensive learning project. It analyzes a password locally, explains predictable patterns, and suggests safer habits. Submitted values are processed transiently; they are not logged or persisted, and the app does not call external breach services.

> Use synthetic examples only. This educational heuristic is not a guarantee that a password is safe. Never enter a real password into a demo or screenshot.

## Problem and objectives

Short, reused, common, and pattern-based passwords can be guessed more easily. A checklist that rewards uppercase + lowercase + digit + symbol can still rate `Password123!` too highly. This project demonstrates length, unpredictability, pattern resistance, common-password checks, optional context, and privacy-conscious design.

## Simple and technical explanation

Password strength is an estimate of how difficult a secret may be to guess. Longer randomly selected secrets generally offer more possibilities; predictable words, keyboard walks, sequences, repeated characters, years, and reuse reduce practical guessing resistance. Entropy is a mathematical model of uncertainty, not a promise. Passphrases made of randomly selected words can be easier to remember. MFA adds another barrier even when a password is exposed.

At a technical level, this application extracts length and character metrics, checks a small local educational common list, detects selected patterns, estimates theoretical entropy, applies a transparent project-defined scoring heuristic, and generates specific findings and advice. No cracking or external leak check is performed.

```text
Browser → Local Flask API → In-memory analysis modules → score / policy / suggestions → browser
                                                  └→ optional metadata-only SQLite analytics
```

## Cybersecurity relevance

Authentication verifies identity; authorization decides what that identity may do. Password controls matter in banking, commerce, enterprise and cloud portals, IAM systems, customer registration, employee accounts, and password managers. Reuse enables credential stuffing, where exposed username/password pairs are tried on other services. Real systems also need password hashing, MFA, rate limiting, abuse protection, safe sessions, phishing defenses, and monitoring.

This project demonstrates skills relevant to Cybersecurity Analyst, Application Security Analyst, IAM Analyst, Security Engineer, SOC Analyst, and Secure Software Developer roles: threat-aware validation, safe data handling, API design, secure randomness, pattern analysis, privacy, testing, and clear security education.

## Password security fundamentals

- **Plaintext vs hash:** plaintext is directly readable; a hash is a one-way verifier. Production services should not store plaintext.
- **Salt and password hashing:** use a unique salt and deliberately expensive password hashing such as Argon2id, bcrypt, scrypt, or PBKDF2. Fast general-purpose hashes alone are unsuitable for password storage.
- **Encryption vs hashing:** encryption is reversible with a key; hashing is designed for one-way verification.
- **Reuse and credential stuffing:** use unique values per account; a manager can generate and remember them.
- **MFA:** another factor protects accounts when a password is guessed, phished, or exposed.
- `backend/services/hash_demo.py` is a separate Argon2id teaching example. It uses only a synthetic hard-coded demonstration and is not connected to arbitrary analyzer input.

## Features

- Real-time hidden-by-default input and show/hide control
- Length bands, case/digit/symbol/space flags, unique count and ratio
- Small local common-password demo list
- Sequence, keyboard-walk, repeated-character, repeated-substring, common-word, trailing-number, year, and optional context checks
- 0–100 heuristic with VERY WEAK / WEAK / MODERATE / STRONG / VERY STRONG classifications
- Policy pass/fail shown separately (example policy: minimum 12, common list rejected)
- Specific security suggestions; theoretical entropy caveat
- 16/20/24-character `secrets` generator
- Optional metadata-only SQLite analytics, disabled by default
- JSON APIs: `POST /api/analyze`, `GET /api/dashboard/stats`, `GET /api/analytics/weaknesses`, `POST /api/generate-password`

## Architecture and folders

`backend/services/` contains independent analyzer, pattern, entropy, suggestion, generator, and analytics modules. `backend/app.py` exposes Flask endpoints. `frontend/` holds the HTML, CSS, and JavaScript UI. `data/common_passwords.txt` contains a tiny educational list, not leaked credentials. `tests/` contains automated tests. `docs/` contains the report and portfolio/interview material. `screenshots/` is reserved for manually captured synthetic examples. `data/analytics.sqlite3` is ignored by Git.

## Scoring and entropy limitations

Points are allocated to length (up to 35), diversity (15), uniqueness ratio (10), pattern resistance (20), a non-common match (10), and an additional unpredictability heuristic (10), then pattern/context/common penalties apply. Bands are project-defined and are not universal standards. Character diversity helps but does not replace unpredictability. Theoretical entropy is `L × log2(N)` based on a rough pool and assumes independent uniformly random choices; human choices violate that assumption. No exact crack-time claim is made.

## Installation and local execution

PowerShell commands from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python backend\app.py
```

Open `http://127.0.0.1:5000`. Type a synthetic demo such as `123456`, `Password123!`, `aaaaaaaaaaaaaaaa`, or `qwerty2026!`. For a random demo, click **Generate** and analyze the result. Do not reuse examples. `secrets` is used instead of `random` because it draws from a cryptographically secure source.

To enable metadata-only analytics, stop the server and set `$env:ENABLE_ANALYTICS="true"` before starting it. Default is off. Clear the generated SQLite file when done. Do not deploy this educational server publicly without HTTPS, request-body log controls, rate limiting, production server hardening, and privacy review.

## API

`POST /api/analyze` accepts JSON `{ "password": "transient value", "context": {"name":"demo"} }`. The response includes score, classification, findings, suggestions, metrics, and policy status, but never returns the input. Use POST body rather than URL parameters. It returns 400 for invalid JSON shape or values beyond 1024 characters; 413 is used when request body exceeds Flask's limit. Generator accepts `{ "length":20 }` with optional enabled groups and permits only lengths 16, 20, or 24. Analytics endpoints return aggregate metadata.

Production deployment must use HTTPS, disable request-body logging at proxies, apply rate limiting, validate inputs, handle errors without secret echo, and review retention/privacy requirements.

## Testing and security testing

Run `pytest -q`. The suite contains 31 cases spanning empty/short/common inputs, character classes, patterns, context, Unicode, spaces, length limits, generator, API-independent result shape, and metadata schema. Recorded unit outcomes are in [docs/TEST_RESULTS.md](docs/TEST_RESULTS.md). Confirm response JSON does not echo input; `analyses` has no password/hash column; frontend source contains no local/session storage or console logging. Inspect network requests: the password is sent only to this local app in a POST body. Analytics are disabled unless explicitly enabled.

## Privacy design and dashboard data model

The analyzer does not log or save passwords, store their hashes, put them in URLs, or persist browser state. Optional SQLite tables hold score, classification, length, unique ratio, weakness count, timestamp, and finding labels only. Hashing arbitrary user-submitted analyzer strings for analytics would still create unnecessary privacy and offline-guessing risks. The stats endpoints aggregate counts, mean score, weakness categories, and length bands.

## Password policies and awareness

Policy compliance is distinct from estimated strength. The sample policy checks a 12-character minimum, common-password list, and optional context; tune it to applicable organizational requirements. Avoid arbitrary periodic changes unless compromise is suspected/confirmed or policy requires them. Ten rules: use unique credentials; prefer length; avoid predictable personal details; avoid common values; never reuse; use a manager; enable MFA; never share; watch for phishing; change compromised credentials.

## Results, limitations, and future work

This is a student demonstration, not a breach detector or production authentication system. The small list and heuristics miss variants and can create false positives. No single formula perfectly judges strength. Future defensive improvements include a reviewed strength-estimation library, configurable enterprise policy, privacy-preserving breach checking, IAM/SSO education, passkey/WebAuthn awareness, localization, accessibility, and aggregate organization reporting without collecting passwords.

## Screenshots and project report

See [docs/PROJECT_REPORT.md](docs/PROJECT_REPORT.md) and [docs/PROOF_OF_WORK.md](docs/PROOF_OF_WORK.md) for the report, screenshot filename checklist, GitHub setup, resume/LinkedIn wording, and exactly ten interview questions with answers. Capture only synthetic values.

## Suggested GitHub setup

Repository: `Password-Strength-Analyzer-Security-Tool`. Description and topics are in `docs/PROOF_OF_WORK.md`. Commands: `git init`, `git add .`, `git commit -m "Initialize password strength analyzer"`, `git branch -M main`, `git remote add origin <repository-url>`, `git push -u origin main`.

## Security disclaimer

Educational defensive tool only. No cracking, account testing, credential collection, or external password transmission is implemented. Do not use real credentials for demonstrations. Strength findings are guidance, not a guarantee.

## Author

SHRADDHA VERMA, B.TECH IN COMPUTER SCIENCE.
