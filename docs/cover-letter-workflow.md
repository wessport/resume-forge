# Cover Letter Workflow

Use this workflow when creating role-specific cover letter PDFs.

## Files

- Save the editable source as Markdown in the job directory:
  - `~/Documents/job_stuff/<company>_<role>/cover_letter_<company>_<role>.md`
- Export the final PDF to the same directory:
  - `~/Documents/job_stuff/<company>_<role>/cover_letter_<company>_<role>.pdf`
- Keep the generated HTML as temporary build output only unless the user explicitly asks to preserve it.

## Layout requirements

- Single A4 page.
- Green accent line: `#70c041`, inset to align with the text margins, never full-bleed to the page edge.
- Include intentional white space above and below the green line; use prior cover letters as the visual reference.
- Header:
  - `Cover Letter` in dark navy (`#1c1d36`), bold, not oversized.
  - `<Role> - <Company>` subtitle in muted gray (`#666666`), regular weight.
- Body uses short paragraphs with bold lead-in phrases, matching prior cover letters.
- Signature block:
  - `Best regards,`
  - `Wesley Porter`
  - `wesporter92@gmail.com`
  - `www.geoalchemist.com`
- Render only the email and website in muted gray (`#666666`). Keep `Best regards,` and `Wesley Porter` in the normal body color.
- Make `www.geoalchemist.com` an actual `https://www.geoalchemist.com` hyperlink in the generated PDF when using HTML-to-PDF.

## PDF generation

Use the checked-in generator script instead of hand-writing temporary HTML/CSS:

```bash
cd /Users/wporter/repos/github/resume-forge
python3 scripts/render_cover_letter.py \
  ~/Documents/job_stuff/<company>_<role>/cover_letter_<company>_<role>.md \
  --subtitle "<Role> - <Company>"
```

By default, the PDF is written next to the Markdown source using the same basename.
Use `--output /path/to/file.pdf` for an explicit output path and `--keep-html` only when debugging layout. Always pass `--subtitle` if the Markdown heading is not already exactly the desired role/company subtitle.

The generator owns the canonical CSS values:

```css
@page { size: A4; margin: 0; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  width: 210mm;
  min-height: 297mm;
  padding: 13.5mm 22mm 13mm 22mm;
  position: relative;
}
.accent {
  width: 100%;
  height: 4px;
  background: #70c041;
  margin: 0 0 9.3mm 0;
}
h1 {
  margin: 0 0 2.2mm 0;
  font-size: 18px;
  line-height: 1.15;
  font-weight: 700;
  color: #1c1d36;
}
.subtitle {
  margin: 0 0 9.8mm 0;
  font-size: 12px;
  line-height: 1.2;
  color: #666666;
  font-weight: 400;
}
.muted {
  color: #666666;
}
```

## Verification

After export:

1. Run `pdfinfo` to confirm the PDF is exactly one page.
2. Run `pdftotext` to confirm text content and ordering.
3. Visually inspect the PDF to confirm:
   - green line is inset to text margins and has white space above/below;
   - title/subtitle sizing, color, and weight match prior cover letters;
   - no clipping or overflow;
   - spacing looks polished;
   - signature block is present, with only email and website muted gray.
