# Video Script - under three minutes

Target length: approximately 2 minutes 40 seconds. Record in English with
audible narration.

## 0:00-0:20 - Problem and audience

**Screen:** Application title and main controls.

**Narration:** "Older local software projects are often hard to restart safely.
Independent developers, solo founders, freelancers, and small teams need a
quick way to see what is missing before editing anything. Codex Project
Recovery Manager V2 turns limited metadata into a recovery plan."

## 0:20-0:42 - Safety boundary

**Screen:** Point to the read-only notice and the visible scrollbar.

**Narration:** "V2 is a standalone Python and Tkinter desktop application. It
examines only names, directory structure, common project markers, Git folder
presence, entry-point names, and modification dates. It never opens file
contents, secrets, credentials, or dot-env contents, and it never changes the
selected project."

## 0:42-1:18 - Needs recovery

**Screen:** Select the direct **Needs recovery** button.

**Narration:** "The Needs recovery demo is entirely synthetic. It has a main
entry point but no README or tests. V2 shows clear evidence and assigns a red
NOW priority with a short explanation. The four-stage plan says: preserve the
folder, understand it by adding guidance, choose the smallest safe
verification, and continue with one bounded Codex task."

## 1:18-1:48 - Safe Codex prompt

**Screen:** Scroll through the four-stage plan to the formatted safe prompt.

**Narration:** "The generated prompt requires a short plan and a list of every
intended file. It forbids delete, move, overwrite, and rename actions without
confirmation. It also forbids reading secrets and requires focused tests or
another safe verification step."

## 1:48-2:12 - Healthy demo and priority colors

**Screen:** Select the direct **Healthy demo** button.

**Narration:** "The Healthy demo includes synthetic README, test, and entry
point markers. It receives an amber LATER priority and explains the remaining
Git metadata evidence. A third gray priority, ARCHIVE FOR CONFIRMATION, is
reserved for an inactive project that should be reviewed before archiving."

## 2:12-2:30 - Export

**Screen:** Select **Export Markdown...**, show the destination dialog, and
cancel it.

**Narration:** "Export is always user-controlled. The report is written only
after a destination is chosen, and it omits the absolute local project path by
default."

## 2:30-2:48 - Tests

**Screen:** Run `python -m unittest discover -s tests -v`.

**Narration:** "The automated suite covers recovery priorities, missing
markers, all four stages, secret-content exclusion, private-path exclusion,
offline demos, friendly labels, readable report text, and priority
presentation."

## 2:48-2:58 - Close

**Screen:** Return to the Recovery Plan.

**Narration:** "Recovery Manager V2 keeps the first move small: preserve,
understand, verify, and only then continue safely with Codex."
