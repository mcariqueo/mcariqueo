# Profile Brief

This file is the living brief for improving my GitHub profile, portfolio page, README, CV, and public research presence.

Use it to capture what I want the profile to communicate, ideas for future improvements, content that should be added, and decisions that should be respected when making changes.

## Main Goal

Present a professional, clear, and credible profile at the intersection of:

- Clinical Pharmacy
- Translational Medicine
- PK/PD and Pharmacometrics
- Critical Care
- Anti-infective therapy
- Clinical Research
- Real-World Evidence
- Healthcare Data Science

The profile should feel serious, academic, biomedical, and modern. It should not feel like a generic tech landing page or an exaggerated marketing site.

## Target Audience

- Research groups in respiratory infections, critical care, pharmacology, and translational medicine.
- Clinical trial teams and clinical research networks.
- Academic collaborators.
- Hospital pharmacy and infectious diseases professionals.
- Data science or clinical analytics teams in healthcare.
- Recruiters or institutions reviewing my research/technical profile.

## Tone And Style

- Professional but human.
- Clear, concise, and evidence-based.
- International English.
- Biomedical and academic, not startup-style.
- Avoid oversized typography, excessive hero sections, bright gradients, or decorative effects.
- Prefer compact sections, clean spacing, and readable hierarchy.

## What The Profile Should Emphasize

- Current PhD work in Translational Medicine.
- IDIBAPS / Hospital Clinic Barcelona environment.
- PK/PD and population pharmacokinetics.
- Therapeutic drug monitoring and model-informed dosing.
- Severe respiratory infections and pneumonia.
- Anti-infective optimization in complex or critically ill patients.
- Clinical trial coordination and REDCap workflows.
- Real-world clinical data analysis.
- Publications, awards, talks, posters, and research output.
- Technical tools: R, Python, SQL, REDCap, NONMEM, PsN.

## What To Avoid

- Overly large text.
- Generic motivational language.
- Long paragraphs that are hard to scan.
- Design that looks like a commercial SaaS landing page.
- Claims that are not supported by CV, publications, institutional profile, or source materials.
- Uploading confidential clinical data, patient data, restricted protocols, or unpublished private documents.

## Portfolio Page Ideas

- Add a concise publications section with selected publications.
- Add a compact "Selected Projects" section:
  - Population PK/PD modeling
  - Clinical trial coordination
  - Real-world pneumonia cohort analysis
  - TDM / anti-infective optimization
- Add a "Methods" section with tools and workflows.
- Add a small "Research Identity" summary.
- Add links to ORCID, ResearchGate, LinkedIn, GitHub, CV, and institutional profile.
- Add a social preview image for LinkedIn sharing.

## README Ideas

- Keep README shorter than the website.
- Use README as a quick professional summary.
- Link to portfolio page, CV, publications, and source materials.
- Keep badges useful and restrained.

## Source Materials Workflow

Use `source-materials/` for public or shareable content that can improve the profile.

Use `private-materials/` for local-only private content. This folder is ignored by Git.

Useful source material to add:

- Updated CVs
- Publication lists
- DOI links
- ORCID exports
- Poster titles
- Conference presentations
- Awards
- Project summaries
- Short bios in English and Spanish
- Teaching experience
- Certifications

## Publication Automation

Publications can be refreshed with:

```bash
python scripts/fetch_publications.py
```

Generated files:

- `source-materials/publications/publications.md`
- `source-materials/publications/publications.json`

The generated publication list should be reviewed manually before being used prominently on the public page.

## Pending Ideas

- [ ] Review generated publication list and mark selected/high-impact publications.
- [ ] Add ORCID link to website footer.
- [ ] Add institutional profile link.
- [ ] Add a selected publications section to `index.html`.
- [ ] Add a compact projects section.
- [ ] Create a LinkedIn/social preview image.
- [ ] Consider bilingual summary: English main, Spanish optional.
- [ ] Add last updated date to portfolio page.

## Design Preferences

- Compact header.
- Moderate font sizes.
- White/light gray background.
- Deep blue, teal, and restrained accent colors.
- Simple cards only when useful.
- No huge marketing hero.
- No heavy gradients.
- No excessive animations.

## Notes For Future Updates

Add new ideas below this line before making major profile changes.

### New Ideas

- 
