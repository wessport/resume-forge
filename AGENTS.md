# Resume Forge — Agent Guidelines

## Git Workflow

- **Never push directly to `main`.** Create a feature branch for changes and use a pull request/merge request workflow instead of pushing commits directly to `main`.
- **Use Wesley's author identity for commits in this repo:**
  - Name: `wessport`
  - Email: `wesporter92@gmail.com`
- **Commit with explicit clean metadata:**
  ```bash
  GIT_AUTHOR_NAME="wessport" GIT_AUTHOR_EMAIL="wesporter92@gmail.com" \
  GIT_COMMITTER_NAME="wessport" GIT_COMMITTER_EMAIL="wesporter92@gmail.com" \
  git commit --no-verify -m "message"
  ```
- **Do not include AI assistant metadata in commits or pull requests.** Avoid co-author trailers, Amp/thread references, ampcode URLs, or any similar AI-assistant metadata.
- **Before pushing any branch, verify new commit messages are clean:**
  ```bash
  git log origin/$(git branch --show-current)..HEAD --format=%B | \
    grep -E 'Co-authored-by: Amp|Amp-Thread-ID|ampcode' && \
    echo "ERROR: forbidden AI metadata found"
  ```
  If the command prints forbidden metadata, rewrite the affected commit message before pushing.
- **After pushing a feature branch, stop and give Wesley the pull request link.** Do not continue to the next task, create follow-up commits, or attempt merge-related actions until Wesley reviews the PR link and gives explicit next instructions.
- **Do not merge pull requests without explicit user approval.** Opening, updating, reviewing, and summarizing PRs is fine; stop before merge unless the user clearly approves that specific merge.

## SVG Templates

- **Never edit existing SVG template files directly.** Always create a new copy with a descriptive name (e.g., `wporter_resume_de_focus.svg`) and make changes there. The originals serve as base templates.
- **Always visually confirm changes** using the `web-browser` skill after editing an SVG. Check for text overflow, layout issues, and overall appearance before reporting the work as done.
- **Check section icon alignment after layout edits.** If you move section headers, bullets, education entries, or any `y` positions to fix spacing, also verify and adjust the corresponding section icon transforms (`objective-icon`, `skills-icon`, `experience-icon`, `education-icon`) so icons remain vertically aligned with their header text.
- **Preserve the one-page resume layout.** When tightening or expanding content, maintain consistent bullet spacing, section spacing, margins, and the existing green header/contact styling unless the user explicitly requests a design change.
- **Use honest slash-title framing where helpful.** For role-specific positioning, prefer truthful slash titles such as `Senior Data Analyst / Analytics Engineer` when they improve keyword alignment without misrepresenting official work history.

## Skills Section

- **Bold skill-category prefixes.** In role-specific resume SVGs, format skill lines with only the category prefix before the colon in bold (for example, `Python & SQL:`), while keeping the detailed keywords after the colon in normal weight.
- **Keep skill details compact and specific.** Prefer high-signal keywords tied to the target job and Wesley's actual work. Avoid vague filler such as "data prep" unless it is an explicit, valuable job-posting keyword.
- **Use categorized skill lines.** Favor compact category labels plus concrete detail over undifferentiated keyword lists, so recruiters can scan both domain and tooling quickly.

## Cover Letter PDFs

- **Green accent line:** Always include a `#70c041` green line near the top of cover letter PDFs. It must be inset to match the text margins, not full-bleed to the page edge, with appropriate white space above and below.
- **Header styling:** Match prior cover letters: dark navy `Cover Letter` title, muted gray regular-weight role/company subtitle, and no oversized header text.
- **Signature block:** Include website `www.geoalchemist.com` below the email in the signature block. Keep `Best regards,` and `Wesley Porter` in normal body color; render only the email and website in muted gray.
- **Use the cover letter generator:** Create cover letter PDFs with `scripts/render_cover_letter.py`; do not hand-write one-off HTML/CSS unless debugging the generator. Follow `docs/cover-letter-workflow.md`.

## Job Application Workflow

- **Always save the original job description** as a markdown file in the corresponding `~/Documents/job_stuff/<company>_<role>/` directory before starting resume/cover letter tailoring.
- **Always sync final application materials** back to the corresponding `~/Documents/job_stuff/<company>_<role>/` directory. After creating or exporting role-specific resume/cover letter SVGs or PDFs in `resume-forge`, copy the final versions into that job-specific directory as well.
