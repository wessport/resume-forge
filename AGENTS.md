# Resume Forge — Agent Guidelines

## Git Workflow

- **Never push directly to `main`.** Create a feature branch for changes and use a pull request/merge request workflow instead of pushing commits directly to `main`.

## SVG Templates

- **Never edit existing SVG template files directly.** Always create a new copy with a descriptive name (e.g., `wporter_resume_de_focus.svg`) and make changes there. The originals serve as base templates.
- **Always visually confirm changes** using the `web-browser` skill after editing an SVG. Check for text overflow, layout issues, and overall appearance before reporting the work as done.
- **Check section icon alignment after layout edits.** If you move section headers, bullets, education entries, or any `y` positions to fix spacing, also verify and adjust the corresponding section icon transforms (`objective-icon`, `skills-icon`, `experience-icon`, `education-icon`) so icons remain vertically aligned with their header text.

## Cover Letter PDFs

- **Green accent line:** Always include a `#70c041` green line across the top of cover letter PDFs to match the resume branding.
- **Signature block:** Include website `www.geoalchemist.com` below the email in the signature block.

## Job Application Workflow

- **Always save the original job description** as a markdown file in the corresponding `~/Documents/job_stuff/<company>_<role>/` directory before starting resume/cover letter tailoring.
- **Always sync final application materials** back to the corresponding `~/Documents/job_stuff/<company>_<role>/` directory. After creating or exporting role-specific resume/cover letter SVGs or PDFs in `resume-forge`, copy the final versions into that job-specific directory as well.
