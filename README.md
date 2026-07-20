# Codex Project Recovery Manager V2

Codex Project Recovery Manager V2 is a standalone Windows desktop application
that turns limited project metadata into a clear, read-only Recovery Plan. It
helps a developer see what may be missing, choose an understandable priority,
and prepare one bounded next task for Codex without changing the audited
project.

> Codex Project Recovery Manager V2 is a new standalone competition project
> inspired by a real project-management need from the author’s earlier work.

The earlier work is the public
[Program-MENAGER](https://github.com/BartekGrabas/Program-MENAGER) repository.
That repository is inspiration only. It is not part of V2, was not claimed as
hackathon work, and no old application data, private folders, credentials, or
real project records were copied into this project.

## Who it is for

V2 is intended for:

- independent developers returning to older local software projects;
- solo founders reviewing paused prototypes;
- freelancers organizing inherited or dormant local codebases; and
- small teams deciding how to restart older internal projects safely.

## What it does

- Audits a selected folder or one of two bundled synthetic demos.
- Shows evidence based on missing or potentially risky metadata.
- Assigns one visible priority:
  - red **NOW** for an immediate recovery gap;
  - amber **LATER** when the project has enough structure for a later review;
  - gray **ARCHIVE FOR CONFIRMATION** when an inactive project may be archived
    after human confirmation.
- Builds a four-stage Recovery Plan: Preserve, Understand, Verify, Continue.
- Generates a safe Codex prompt that requires a short plan, intended-file
  list, confirmation before destructive actions, secret avoidance, and a
  focused verification step.
- Exports a Markdown report only after the user chooses a destination.

## Read-only, metadata-only safety

The audit examines metadata only:

- file and folder names;
- directory structure;
- presence of README, tests, Git metadata, and conventional entry points; and
- modification dates.

It never opens source-file contents, `.env` contents, credentials, tokens,
passwords, keys, or customer documents. It does not modify the selected
project, follow directory symlinks, or inspect Git internals, dependency trees,
virtual environments, caches, or secret-oriented directories.

The generated report uses the selected folder's final name as a label and
omits its absolute path by default. V2 is a planning aid, not a backup tool or
security scanner. A person should review every recommendation before making
project changes.

## Requirements

- Windows 10 or later
- Python 3.10 or later with Tkinter

Tkinter is included with standard Windows Python installations from
[python.org](https://www.python.org/). V2 uses only the Python standard library.

No API key, online account, external service, network connection, third-party
Python package, or real project data is needed.

## Install

1. Install Python 3.10 or later for Windows if it is not already available.
2. Obtain this project folder after the repository is published, or use the
   local competition copy.
3. Open PowerShell in the project folder.
4. Optionally confirm Python is available:

```powershell
python --version
```

There is no package installation command because the application has no
third-party dependencies.

## Run

```powershell
python app.py
```

The desktop window opens with project selection, two direct demo buttons, a
general demo chooser, and Markdown export.

## Use the synthetic demos

No real project folder is required for the demonstration.

1. Select **Healthy demo** to inspect the internal `healthy_demo` folder. It
   contains synthetic README, test, and entry-point markers. The interface
   assigns **LATER** priority and explains the remaining Git metadata evidence.
2. Select **Needs recovery** to inspect the internal `needs_recovery` folder.
   It intentionally lacks README and test markers. The interface assigns
   **NOW** priority and proposes a four-stage recovery sequence.
3. Alternatively, select **Load synthetic demo** and choose either friendly
   demo name from the list.
4. Scroll through the evidence, metadata summary, Recovery Plan, and generated
   safe prompt.
5. Select **Export Markdown...** only if you want to save a report to a
   destination you choose.

Both demos are invented, public-safe, offline, and credential-free.

## Audit a local project

Select **Select project folder** and choose a folder. V2 lists only the allowed
metadata described above. The selected project is never changed.

Do not use a real project for the competition demo; the bundled synthetic
projects demonstrate the complete workflow without exposing private data.

## Test

Run the complete standard-library test suite:

```powershell
python -m unittest discover -s tests -v
```

Tests cover unavailable-folder priority, missing recovery markers, the
four-stage plan, secret-content exclusion, private-path exclusion, offline
demos, friendly demo labels, readable desktop report text, and priority
presentation.

## Codex and GPT-5.6 collaboration

This V2 implementation was developed in the primary competition Codex thread.
The participant explicitly confirmed that GPT-5.6 was selected for that thread
before implementation continued. Codex assisted with implementation, tests,
documentation, and local verification under participant-defined requirements.
This is a user-confirmed selection statement and does not claim access to
hidden model telemetry.

No `/feedback` Session ID is recorded here. After core V2 work is complete, the
participant will run `/feedback` in this same clean V2 thread and add only the
real resulting Session ID to the competition submission.

## Publication status

The intended repository URL is
<https://github.com/BartekGrabas/codex-project-recovery-manager-v2>. Creating
that GitHub repository, committing or pushing code, uploading a video, and
submitting to Devpost require explicit participant approval and are not part of
this local documentation review.

## License

MIT - see [LICENSE](LICENSE).
