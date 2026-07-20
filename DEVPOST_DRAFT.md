# Devpost Draft - Codex Project Recovery Manager V2

## Tagline

Turn limited project metadata into a safe, bounded recovery plan before
editing anything.

## Inspiration

Returning to an older local software project often starts with uncertainty:
Is this the correct folder? Is there usable documentation? Are tests present?
What is the smallest safe next step?

Codex Project Recovery Manager V2 is a new standalone competition project
inspired by a real project-management need from the author’s earlier work.
The reference is the public
[Program-MENAGER](https://github.com/BartekGrabas/Program-MENAGER) repository.
It is inspiration only. The older application was not claimed as hackathon
work, is not part of V2, and none of its data, private folders, credentials, or
real project records were copied into V2.

The intended users are independent developers, solo founders, freelancers,
and small teams returning to older local software projects.

## What it does

Recovery Manager V2 is a Windows desktop application built with Tkinter. The
user selects a project folder or one of two bundled synthetic demos. The
application examines names, directory structure, conventional marker presence,
Git directory presence, entry-point names, and modification dates. It does not
open file contents or modify the selected project.

The interface provides:

- evidence of missing or potentially risky metadata;
- a visible red **NOW**, amber **LATER**, or gray
  **ARCHIVE FOR CONFIRMATION** priority with a short explanation;
- a four-stage Preserve, Understand, Verify, and Continue Recovery Plan;
- a constrained Codex prompt for one bounded next task; and
- user-controlled Markdown export that omits the absolute project path by
  default.

The generated prompt requires a short plan and intended-file list, forbids
delete, move, overwrite, and rename actions without confirmation, forbids
reading secrets and `.env` contents, and requires focused verification.

## How it was built

The application uses Python's standard library and Tkinter. Its audit loop uses
`os.scandir` to obtain names, types, and timestamps without opening file
contents. It prunes Git internals, dependency trees, virtual environments,
caches, and secret-oriented directories, and it does not follow directory
symlinks.

The project includes two invented offline demos, a desktop interface with a
visible scrollbar and formatted report sections, Markdown export, and a
standard-library unit test suite.

The participant explicitly confirmed that GPT-5.6 was selected in the primary
V2 Codex competition thread. Codex assisted with implementation, tests,
documentation, and local verification within participant-defined constraints.
This statement records the participant's confirmation and does not claim
access to hidden model telemetry.

## Challenges

The main challenge was producing useful recovery guidance without reading
project contents. V2 treats missing conventional markers as evidence rather
than certainty and keeps recommendations bounded and reviewable.

A second challenge was preventing private information from flowing into the
report or generated prompt. The implementation does not read secret content,
and automated tests verify both secret-content exclusion and omission of an
absolute private project path.

A third challenge was presenting technical evidence clearly in a desktop UI.
The current interface uses friendly demo names, formatted sections, a visible
scrollbar, priority colors, and short priority explanations.

## Accomplishments

- Built a runnable Windows desktop application with no third-party dependency.
- Implemented a read-only, metadata-only audit.
- Produced a visible four-stage Recovery Plan.
- Generated a reusable safety-constrained Codex prompt.
- Added explicit, user-controlled Markdown export.
- Added two public-safe synthetic demos requiring no credentials or services.
- Added automated tests for required safety and presentation behavior.

## What was learned

Recovery tooling can provide value before receiving permission to edit.
Carefully selected metadata is enough to propose a useful first step, while
explicit constraints make a later handoff to an AI coding agent easier to
review.

The project also showed that transparent provenance matters: earlier work can
explain the real need without being presented as new competition output.

## What is next

Possible future work includes configurable marker rules, additional
language-specific entry-point detection, improved accessibility testing, and a
signed Windows package. These are ideas, not current features.

Before submission, the project still needs an approved public or properly
shared repository, a public YouTube demo under three minutes with audio, the
real `/feedback` Session ID from the clean primary V2 thread, and the
participant's explicit approval.

## Built with

- Python 3 standard library
- Tkinter and ttk
- `unittest`
- Codex, with GPT-5.6 selection explicitly confirmed by the participant for
  the primary V2 build thread

No API key, online account, external service, or real project data is required
to run the application or its demos.

## Submission placeholders

- Code repository: pending participant approval and publication
- Public YouTube demo under three minutes with audio: pending
- `/feedback` Session ID from the primary V2 build thread: pending; do not
  invent
- Devpost submission: pending explicit participant approval
