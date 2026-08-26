# Source Materials

Use this folder to store public or shareable material that can help improve the portfolio page, README, CV, and research profile.

Suggested structure:

- `cv/`: CV versions, bios, short profile summaries.
- `publications/`: publication lists, citations, abstracts, DOI links, accepted manuscripts if shareable.
- `certifications/`: public certificates or training records.
- `talks-posters/`: conference posters, slides, oral presentations, awards.
- `projects/`: short notes about research projects, methods, datasets, and outputs.
- `notes/`: raw notes that can later become polished portfolio content.

Avoid uploading files with patient data, confidential study documents, unpublished restricted manuscripts, credentials, private contracts, or institutional material that cannot be shared publicly.

For private local-only files, use the ignored folder:

```text
private-materials/
```

## Updating Publications

Run this command from the repository root to refresh the publication list from ORCID and Crossref:

```bash
python scripts/fetch_publications.py
```

The generated files are:

- `source-materials/publications/publications.md`
- `source-materials/publications/publications.json`
