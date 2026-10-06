# Project Report: Password Strength Analyzer & Security Suggestion Tool

## Abstract
This defensive educational application gives immediate, local feedback on password length, character use, common examples, repetition, keyboard walks, sequences, predictable structures and voluntarily supplied demo context. It combines these signals into a project-defined score, explains limitations, and gives practical advice. Passwords are processed transiently; opt-in analytics persist aggregate metadata only.

## Introduction and problem statement
Passwords remain a common authentication factor, but people often choose short, reused, or predictable strings. Composition checklists can reward choices such as a common word followed by a year. A useful coach needs to explain predictable structure and privacy while avoiding the false claim that a single score proves safety.

## Objectives
- Build a beginner-readable modular Python and Flask application.
- Detect representative predictable patterns locally.
- Separate strength estimate from a configurable example policy.
- Never log or persist submitted passwords or send them to a breach service.
- Provide synthetic-only demonstrations, metadata analytics, and security education.

## Password security background
Authentication establishes identity; authorization decides what an authenticated identity may do. A password is a knowledge factor. A passphrase is a longer password-like secret, ideally made from randomly selected words. Reuse lets credential stuffing (automated attempts of previously exposed pairs on other services) turn one incident into many. A password manager helps create unique values; MFA adds another factor.

Production applications must not store plaintext. They store a salted, deliberately expensive password hash and verify submitted candidates by recomputing the function. Argon2id, bcrypt, scrypt, and PBKDF2 are established password-hashing choices. A general-purpose fast hash such as plain SHA-256 is not suitable alone for password storage. Hashing is one-way verification; encryption is reversible with a key. This project keeps the standalone Argon2id teaching example out of the analyzer and stores no analyzer hash.

## Proposed system and architecture
Browser input → Flask `/api/analyze` over local HTTP → in-memory analyzer modules → score/classification/policy/suggestions → browser UI. If explicitly enabled, safe aggregate fields go to SQLite. Database schema contains analyses and findings, with no password column. The UI does not put inputs in URLs, localStorage, sessionStorage, or console output.

## Analysis, features, patterns, and entropy
The analyzer measures length, upper/lower/digit/symbol/space presence, unique count/ratio, exact common-list matches, short ascending/descending sequences, local keyboard walks, repeated characters/substrings, year/trailing-number structures, and optional context overlap. The common list is a tiny educational local list, not a breach corpus. Sequence detection reports representative four-character substrings; keyboard detection reports local educational examples.

Theoretical entropy is approximated as `L × log2(N)`, with a rough pool inferred from character groups. It assumes independent uniform random selection. Human-generated choices are biased, so values can be very optimistic; pattern findings and length are considered alongside it. There is no exact guaranteed crack-time estimate.

## Strength scoring and recommendations
The 0–100 project score combines length (up to 35), character diversity (15), uniqueness ratio (10), pattern resistance (20), non-common match (10), and an unpredictability contribution (10), with explicit penalties. Bands are project-defined, not standards. Suggestions are code-driven and never echo entered content. Policy pass/fail (minimum 12, common-value check, optional context check) is separate from estimated strength. Change policy configuration in analyzer code for a deployment; an organization should align its policy to its actual requirements.

## Generator and policy
The demo generator accepts 16, 20, or 24 characters and selected character groups. It uses `secrets.choice` plus secure shuffle, not `random`. Generated values are returned once for display/copy; they are not recorded. A random-word passphrase can be both memorable and hard to guess if its words are selected randomly. Avoid famous quotes or reused examples. Do not force periodic changes absent evidence of compromise or a policy requirement.

## Privacy, dashboard, and database
Analytics are disabled by default (`ENABLE_ANALYTICS=false`). When enabled, the SQLite tables contain score, class, length, unique ratio, weakness count, timestamp and finding labels/descriptions. Even hashes of arbitrary analysis inputs would create needless correlation and offline-guessing risk, so none are saved. The dashboard aggregates total, classifications, mean score, weakness labels and length bands. It has no charts dependency in this first implementation; API data can be plotted in a later UI iteration.

## Testing and security testing
`pytest` covers 30 scenarios for edge inputs, detectors, policy-related behavior, generator, Unicode, max size, and metadata schema. Review API responses to confirm no input echo; the frontend uses password input, has no persistence calls, and emits no input to console. Analytics schema inspection verifies the absence of password columns. Request bodies necessarily carry a password from browser to the local Flask process; use HTTPS if deployed remotely, disable request-body logging in any proxy, rate-limit remote deployments, and never expose this demo publicly without production controls.

## Results and limitations
The application gives immediate actionable feedback without storing the analyzed secret. Its tiny common list misses real-world variants; substring heuristics can create false positives/negatives; the score is not a breach check and cannot determine real guessing resistance. Password strength is only one part of login security: MFA, rate limiting, abuse protection, secure password hashing, session controls, phishing resistance, and monitoring all matter.

## Future scope and conclusion
Future defensive work could integrate a maintained estimator, configurable enterprise policy, privacy-preserving breach checks, accessibility/localization, passkey/WebAuthn education, and organization-level aggregate reporting. Any breach integration needs a carefully reviewed privacy protocol. This project demonstrates defensive analysis, secure randomness, privacy-first design, modular Python, Flask APIs, testing, and security awareness while keeping its claims proportionate.
