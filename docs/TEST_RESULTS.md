# Test results

The 31 local unit checks in `tests/test_analyzer.py` were executed using the bundled Python runtime by invoking each test function directly (the runtime did not include pytest). All listed cases passed. Re-run through pytest in a project virtual environment after installing `requirements.txt`.

| ID | Scenario / synthetic input | Expected result | Actual result | Status |
|---|---|---|---|---|
| T01 | Empty string | Score 0 | Score 0 | PASS |
| T02 | One character `x` | Length 1 | Length 1 | PASS |
| T03 | Short numeric `123` | VERY WEAK | VERY WEAK | PASS |
| T04 | Common `password` | Common match true | Match true | PASS |
| T05 | Repeated `aaaaaaaaaaaaaaaa` | Score below 60 | Score 37 | PASS |
| T06 | Lowercase-only synthetic value | Uppercase false | False | PASS |
| T07 | Uppercase-only synthetic value | Uppercase true | True | PASS |
| T08 | Numeric-only synthetic value | Digit true | True | PASS |
| T09 | Symbol-only synthetic value | Symbol true | True | PASS |
| T10 | Mixed `aZ7!rT9#kL2@` | Four character types | Four | PASS |
| T11 | Ascending `ab1234xy` | Detect `1234` | Detected | PASS |
| T12 | Descending `x9876y` | Detect `9876` | Detected | PASS |
| T13 | Ascending letters `abcde` | Detect `abcd` | Detected | PASS |
| T14 | Keyboard `qwerty2026!` | Detect `qwerty` | Detected | PASS |
| T15 | Repeated characters `AAAAAA123!` | Detect repeated characters | Detected | PASS |
| T16 | Repeated substring `abcabcabc` | Detect repeated substring | Detected | PASS |
| T17 | Common word + numbers `welcome123` | Predictable structure finding | Finding returned | PASS |
| T18 | Year-like `Cedar!2026` | Year pattern present | Present | PASS |
| T19 | Context name `Rahul` in `Rahul@123` | Context overlap true | True | PASS |
| T20 | Context year `1988` in `Tree#1988` | Context overlap true | True | PASS |
| T21 | Synthetic phrase with spaces | Length over 20 | 40 | PASS |
| T22 | Unicode `pássphräsé🌲` | Analyze without error | Analyzed | PASS |
| T23 | Space-containing demo phrase | Spaces true | True | PASS |
| T24 | 1024 repeated characters | Accepted at limit | Accepted | PASS |
| T25 | 1025 repeated characters | Rejected | ValueError | PASS |
| T26 | Sample `sample` | Valid classification label | WEAK | PASS |
| T27 | `123456` | Sequence-specific suggestion | Returned | PASS |
| T28 | Generate length 20 | Exactly 20 characters | 20 | PASS |
| T29 | Lowercase-only generator options | Lowercase result | Lowercase result | PASS |
| T30 | Record synthetic analysis in temp SQLite | No password/hash column | No such columns | PASS |
| T31 | Result object for synthetic input | No password field | No password field | PASS |

## Security review checklist

| Check | Expected | Review result |
|---|---|---|
| Database schema | No plaintext or password-hash column | Verified by T30 |
| Analyzer result | Does not return submitted value | Verified by T31 |
| URL handling | Input only in POST JSON body | Frontend source uses fetch POST; no query parameter construction |
| Browser persistence | No localStorage/sessionStorage writes | Source inspection found none |
| Console output | No entered value logging | Source inspection found no console logging |
| Default analytics | Disabled | `ENABLE_ANALYTICS=false` unless explicitly changed |
| External requests | No breach lookup or external password API | Verified; page assets are local and there is no external fetch |
| Full Flask API integration | HTTP client checks | Not run in this workspace: Flask/pytest packages are not installed in the bundled interpreter |

Install `requirements.txt` in a virtual environment, then run `pytest -q` and manually inspect responses with synthetic inputs before publishing. This report does not claim API integration tests were run.
