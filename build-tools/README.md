# Build Tools

This folder contains scripts and documentation files used during the development and conversion of articles.

## Contents:

### Conversion Script
- **convert_articles.py** - Python script that converts markdown articles to HTML format
  - Handles markdown formatting (headers, lists, links, code blocks)
  - Automatically converts .md links to .html
  - Generates complete HTML pages with navigation and styling

### Documentation Files
- **UPDATE_SUMMARY.md** - Summary of article update process (November 7, 2025)
- **LINKS_VERIFICATION.md** - Verification report for all article links

## Usage:

To convert articles from markdown to HTML:

```bash
python convert_articles.py
```

or on Windows:

```bash
py convert_articles.py
```

The script will:
1. Read all article-X-REWRITTEN.md files from articles/archive/
2. Convert markdown to HTML
3. Generate article-X.html files in articles/
4. Apply consistent styling and navigation

---
Created: November 7, 2025
