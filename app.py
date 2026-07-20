"""Codex Project Recovery Manager V2.

A read-only metadata audit and recovery-plan generator with a Tkinter UI.
The audit deliberately does not read file contents.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


APP_TITLE = "Codex Project Recovery Manager V2"
MAX_ENTRIES = 5_000
README_NAMES = {"readme", "readme.md", "readme.rst", "readme.txt"}
ENTRY_POINT_NAMES = {
    "app.py",
    "main.py",
    "manage.py",
    "server.py",
    "index.html",
    "package.json",
    "pyproject.toml",
}
PRUNED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    "secrets",
    "private",
}
SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.json",
}
DEMO_DISPLAY_NAMES = {
    "healthy_demo": "Healthy demo",
    "needs_recovery": "Needs recovery",
}
PRIORITY_PRESENTATION = {
    "now": (
        "NOW",
        "priority_now",
        "Act now: important recovery guidance or project access is missing.",
    ),
    "later": (
        "LATER",
        "priority_later",
        "Review later: the project has enough structure for a safe follow-up.",
    ),
    "archive for confirmation": (
        "ARCHIVE FOR CONFIRMATION",
        "priority_archive",
        "Confirm before archiving: the project appears inactive.",
    ),
}


@dataclass(frozen=True)
class AuditResult:
    """A privacy-safe audit result containing no absolute project path."""

    project_name: str
    available: bool
    priority: str
    evidence: tuple[str, ...]
    recovery_plan: tuple[tuple[str, str], ...]
    codex_prompt: str
    metadata_summary: tuple[str, ...]

    def to_markdown(self) -> str:
        evidence = "\n".join(f"- {item}" for item in self.evidence)
        plan = "\n".join(
            f"{index}. **{stage}:** {action}"
            for index, (stage, action) in enumerate(self.recovery_plan, start=1)
        )
        metadata = "\n".join(f"- {item}" for item in self.metadata_summary)
        return (
            f"# Recovery report: {self.project_name}\n\n"
            f"**Priority:** {self.priority}\n\n"
            "## Evidence\n\n"
            f"{evidence}\n\n"
            "## Metadata summary\n\n"
            f"{metadata}\n\n"
            "## Recovery Plan\n\n"
            f"{plan}\n\n"
            "## Safe Codex prompt\n\n"
            "```text\n"
            f"{self.codex_prompt}\n"
            "```\n"
        )


def _safe_project_name(path: Path) -> str:
    """Return a display label without exposing an absolute path."""

    name = path.name.strip()
    return name if name and name not in {".", os.sep} else "Selected project"


def _age_in_days(timestamp: float, now: datetime) -> int:
    modified = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return max(0, (now - modified).days)


def _iter_metadata(root: Path) -> Iterable[tuple[str, bool, float]]:
    """Yield relative names, directory flags, and mtimes without opening files."""

    seen = 0
    stack = [root]
    while stack and seen < MAX_ENTRIES:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    if seen >= MAX_ENTRIES:
                        return
                    seen += 1
                    relative = Path(entry.path).relative_to(root).as_posix()
                    try:
                        is_directory = entry.is_dir(follow_symlinks=False)
                        modified = entry.stat(follow_symlinks=False).st_mtime
                    except OSError:
                        yield relative, False, 0.0
                        continue
                    yield relative, is_directory, modified
                    if is_directory and entry.name.lower() not in PRUNED_DIRECTORIES:
                        stack.append(Path(entry.path))
        except OSError:
            continue


def _build_plan(
    project_name: str,
    available: bool,
    has_readme: bool,
    has_tests: bool,
    entry_points: list[str],
) -> tuple[tuple[str, str], ...]:
    if not available:
        understand = "Restore or reselect the folder, then inspect its metadata again."
        verify = "Confirm that the folder exists and can be listed read-only."
    else:
        understand = (
            "Review the existing README and run instructions."
            if has_readme
            else "Add a concise README with purpose, setup, and run instructions."
        )
        if has_tests:
            verify = "Run the smallest existing test target without changing project files."
        elif entry_points:
            verify = (
                f"Choose a non-destructive check for the detected entry point "
                f"`{entry_points[0]}`."
            )
        else:
            verify = "Define one minimal smoke check before making functional changes."
    return (
        (
            "Preserve",
            f"Confirm the folder for `{project_name}` and make no destructive changes.",
        ),
        ("Understand", understand),
        ("Verify", verify),
        (
            "Continue",
            "Give Codex one bounded task after reviewing the evidence and verification result.",
        ),
    )


def _build_prompt(
    project_name: str,
    available: bool,
    has_readme: bool,
    has_tests: bool,
) -> str:
    suggested_files: list[str] = []
    if available and not has_readme:
        suggested_files.append("README.md")
    if available and not has_tests:
        suggested_files.append("tests/<new focused test file>")
    intended = ", ".join(suggested_files) if suggested_files else "none until reviewed"
    return (
        f"Work on the selected project `{project_name}` using a preservation-first approach.\n"
        "Before editing, provide a short plan.\n"
        f"List every intended file to change; initial candidates: {intended}.\n"
        "Do not delete, move, overwrite, or rename anything without my explicit confirmation.\n"
        "Do not read or reveal secrets, credentials, tokens, passwords, keys, customer "
        "documents, or any .env file contents.\n"
        "Inspect only the metadata and files needed for the bounded task.\n"
        "After any approved edit, run focused tests or another safe verification step and "
        "report the exact result."
    )


def audit_project(project_folder: str | os.PathLike[str]) -> AuditResult:
    """Audit a project using filesystem metadata only."""

    path = Path(project_folder)
    name = _safe_project_name(path)
    now = datetime.now(timezone.utc)

    if not path.is_dir():
        evidence = ("Project folder is unavailable or is not a directory.",)
        plan = _build_plan(name, False, False, False, [])
        prompt = _build_prompt(name, False, False, False)
        return AuditResult(
            project_name=name,
            available=False,
            priority="now",
            evidence=evidence,
            recovery_plan=plan,
            codex_prompt=prompt,
            metadata_summary=("No project metadata was scanned.",),
        )

    names: list[str] = []
    directories: set[str] = set()
    latest_timestamp = 0.0
    sensitive_markers = 0
    for relative, is_directory, modified in _iter_metadata(path):
        names.append(relative)
        latest_timestamp = max(latest_timestamp, modified)
        leaf = Path(relative).name.lower()
        if is_directory:
            directories.add(leaf)
        if leaf in SENSITIVE_NAMES or leaf.startswith(".env."):
            sensitive_markers += 1

    lower_files = {Path(item).name.lower() for item in names}
    has_readme = bool(lower_files & README_NAMES)
    has_tests = (
        "tests" in directories
        or "test" in directories
        or any(
            leaf.startswith("test_") and leaf.endswith(".py")
            for leaf in lower_files
        )
    )
    has_git = (path / ".git").is_dir()
    entry_points = sorted(lower_files & ENTRY_POINT_NAMES)
    age_days = _age_in_days(latest_timestamp, now) if latest_timestamp else 0

    evidence_list: list[str] = []
    if not has_readme:
        evidence_list.append("README or equivalent project guidance is missing.")
    if not has_tests:
        evidence_list.append("No tests directory or conventional Python test file was found.")
    if not has_git:
        evidence_list.append("Git metadata was not detected.")
    if not entry_points:
        evidence_list.append("No conventional application entry point was detected.")
    if age_days >= 365:
        evidence_list.append(
            f"Newest detected metadata timestamp is approximately {age_days} days old."
        )
    if sensitive_markers:
        evidence_list.append(
            "Sensitive-file markers were detected; their contents were not opened or reported."
        )
    if not evidence_list:
        evidence_list.append("No immediate recovery gaps were detected from metadata.")

    if not has_readme or not has_tests:
        priority = "now"
    elif age_days >= 365:
        priority = "archive for confirmation"
    else:
        priority = "later"

    metadata = (
        f"Entries inspected: {len(names)} (limit {MAX_ENTRIES}).",
        f"README detected: {'yes' if has_readme else 'no'}.",
        f"Tests detected: {'yes' if has_tests else 'no'}.",
        f"Git metadata detected: {'yes' if has_git else 'no'}.",
        "Entry points detected: "
        + (", ".join(entry_points) if entry_points else "none"),
        "File contents read: no.",
    )
    plan = _build_plan(name, True, has_readme, has_tests, entry_points)
    prompt = _build_prompt(name, True, has_readme, has_tests)
    return AuditResult(
        project_name=name,
        available=True,
        priority=priority,
        evidence=tuple(evidence_list),
        recovery_plan=plan,
        codex_prompt=prompt,
        metadata_summary=metadata,
    )


def export_report(result: AuditResult, destination: str | os.PathLike[str]) -> None:
    """Export a report only to the destination explicitly supplied by the user."""

    Path(destination).write_text(result.to_markdown(), encoding="utf-8")


def demo_project_paths() -> list[Path]:
    demo_root = Path(__file__).resolve().parent / "demo_projects"
    if not demo_root.is_dir():
        return []
    return sorted(
        (item for item in demo_root.iterdir() if item.is_dir()),
        key=lambda item: item.name.lower(),
    )


def demo_display_name(technical_name: str) -> str:
    """Return a friendly UI label while keeping the folder name unchanged."""

    return DEMO_DISPLAY_NAMES.get(
        technical_name, technical_name.replace("_", " ").strip().title()
    )


def priority_presentation(priority: str) -> tuple[str, str, str]:
    """Return the visible label, Tk tag, and short explanation for a priority."""

    return PRIORITY_PRESENTATION.get(
        priority,
        (
            priority.upper(),
            "priority_archive",
            "Review this priority before continuing.",
        ),
    )


def report_display_chunks(result: AuditResult) -> tuple[tuple[str, str], ...]:
    """Build readable tagged UI text without Markdown presentation symbols."""

    priority_label, priority_tag, priority_explanation = priority_presentation(
        result.priority
    )
    chunks: list[tuple[str, str]] = [
        ("Project\n", "section"),
        (f"{demo_display_name(result.project_name)}\n\n", "project"),
        ("Priority\n", "section"),
        (f"{priority_label}\n", priority_tag),
        (f"{priority_explanation}\n\n", "body"),
        ("Evidence\n", "section"),
    ]
    chunks.extend((f"• {item}\n", "body") for item in result.evidence)
    chunks.extend(
        [
            ("\nMetadata summary\n", "section"),
            *[(f"• {item}\n", "body") for item in result.metadata_summary],
            ("\nRecovery Plan\n", "section"),
        ]
    )
    chunks.extend(
        (
            f"{index}. {stage}: {action.replace('`', '')}\n",
            "body",
        )
        for index, (stage, action) in enumerate(result.recovery_plan, start=1)
    )
    chunks.extend(
        [
            ("\nSafe Codex prompt\n", "section"),
            (result.codex_prompt.replace("`", "") + "\n", "prompt"),
        ]
    )
    return tuple(chunks)


class RecoveryManagerApp:
    def __init__(self, root: object) -> None:
        import tkinter as tk
        from tkinter import ttk

        self.root = root
        self.current_result: AuditResult | None = None
        root.title(APP_TITLE)
        root.geometry("900x680")
        root.minsize(720, 520)

        header = ttk.Frame(root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text=APP_TITLE, font=("Segoe UI", 16, "bold")).pack(
            side="left"
        )
        controls = ttk.Frame(root, padding=(12, 0, 12, 8))
        controls.pack(fill="x")
        ttk.Button(controls, text="Select project folder", command=self.select_folder).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(
            controls,
            text="Healthy demo",
            command=lambda: self.load_demo("healthy_demo"),
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            controls,
            text="Needs recovery",
            command=lambda: self.load_demo("needs_recovery"),
        ).pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Load synthetic demo", command=self.select_demo).pack(
            side="left", padx=(0, 8)
        )
        self.export_button = ttk.Button(
            controls, text="Export Markdown…", command=self.export_current, state="disabled"
        )
        self.export_button.pack(side="left")
        ttk.Label(
            root,
            text=(
                "Read-only audit: names, marker presence, directory structure, and dates only. "
                "File contents are never opened."
            ),
            padding=(12, 0, 12, 8),
        ).pack(fill="x")
        output_frame = ttk.Frame(root)
        output_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.output = tk.Text(
            output_frame,
            wrap="word",
            padx=14,
            pady=12,
            font=("Segoe UI", 10),
            borderwidth=1,
            relief="solid",
        )
        self.output_scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output.yview
        )
        self.output.configure(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.pack(side="right", fill="y")
        self.output.pack(side="left", fill="both", expand=True)
        self.output.tag_configure(
            "section",
            font=("Segoe UI", 11, "bold"),
            foreground="#1f2937",
            spacing1=6,
            spacing3=3,
        )
        self.output.tag_configure(
            "project", font=("Segoe UI", 14, "bold"), foreground="#111827"
        )
        self.output.tag_configure(
            "priority_now",
            font=("Segoe UI", 12, "bold"),
            foreground="#c62828",
        )
        self.output.tag_configure(
            "priority_later",
            font=("Segoe UI", 12, "bold"),
            foreground="#b26a00",
        )
        self.output.tag_configure(
            "priority_archive",
            font=("Segoe UI", 12, "bold"),
            foreground="#6b7280",
        )
        self.output.tag_configure("body", spacing1=1, spacing3=1)
        self.output.tag_configure(
            "prompt",
            background="#f3f4f6",
            foreground="#111827",
            lmargin1=12,
            lmargin2=12,
            spacing1=6,
            spacing3=6,
        )
        self.output.insert(
            "1.0",
            "Choose a project folder or a bundled synthetic demo to create a Recovery Plan.",
        )
        self.output.configure(state="disabled")

    def _show_result(self, result: AuditResult) -> None:
        self.current_result = result
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        for text, tag in report_display_chunks(result):
            self.output.insert("end", text, tag)
        self.output.see("1.0")
        self.output.configure(state="disabled")
        self.export_button.configure(state="normal")

    def select_folder(self) -> None:
        from tkinter import filedialog

        selected = filedialog.askdirectory(title="Select a project folder")
        if selected:
            self._show_result(audit_project(selected))

    def load_demo(self, technical_name: str) -> None:
        from tkinter import messagebox

        selected = next(
            (item for item in demo_project_paths() if item.name == technical_name),
            None,
        )
        if selected is None:
            messagebox.showerror(
                APP_TITLE,
                f"The synthetic demo “{demo_display_name(technical_name)}” is unavailable.",
            )
            return
        self._show_result(audit_project(selected))

    def select_demo(self) -> None:
        import tkinter as tk
        from tkinter import messagebox, ttk

        demos = demo_project_paths()
        if not demos:
            messagebox.showerror(APP_TITLE, "No synthetic demo projects are available.")
            return
        chooser = tk.Toplevel(self.root)
        chooser.title("Choose a synthetic demo")
        chooser.resizable(False, False)
        frame = ttk.Frame(chooser, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Bundled public-safe demo projects:").pack(anchor="w")
        display_to_demo = {demo_display_name(item.name): item for item in demos}
        selection = tk.StringVar(value=demo_display_name(demos[0].name))
        box = ttk.Combobox(
            frame,
            textvariable=selection,
            values=list(display_to_demo),
            state="readonly",
            width=36,
        )
        box.pack(fill="x", pady=10)

        def load() -> None:
            selected = display_to_demo[selection.get()]
            chooser.destroy()
            self._show_result(audit_project(selected))

        ttk.Button(frame, text="Load demo", command=load).pack(anchor="e")
        chooser.transient(self.root)
        chooser.grab_set()

    def export_current(self) -> None:
        from tkinter import filedialog, messagebox

        if self.current_result is None:
            return
        destination = filedialog.asksaveasfilename(
            title="Export Recovery Plan",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md")],
            initialfile="recovery-report.md",
        )
        if destination:
            try:
                export_report(self.current_result, destination)
            except OSError as error:
                messagebox.showerror(APP_TITLE, f"Could not export report: {error}")
            else:
                messagebox.showinfo(APP_TITLE, "Report exported to your chosen destination.")


def main() -> None:
    import tkinter as tk

    root = tk.Tk()
    RecoveryManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
