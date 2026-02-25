# Regex Filter Examples for Migration Report Consolidation

This README explains how to use the regex filter examples provided in `regex_filter_examples.py` with your consolidation script.

## How to Use Regex Filters

The consolidation script uses regex filters to exclude unwanted rows from CSV files. Here are examples for different filtering scenarios:

### 1. Filtering Content at the Beginning of a Line

```python
import re

# Filter rows that start with "Test" (case insensitive)
DOCUMENT_EXPORT_FILTERS = [
    re.compile(r"^Test", re.IGNORECASE),  # ^ anchors to the beginning
]

# Filter rows that start with a number
DOCUMENT_EXPORT_FILTERS = [
    re.compile(r"^\d+"),  # \d+ matches one or more digits
]
```

### 2. Filtering Content at the End of a Line

```python
import re

# Filter rows that end with "pending"
DOCUMENT_IMPORT_FILTERS = [
    re.compile(r"pending$", re.IGNORECASE),  # $ anchors to the end
]

# Filter rows that end with a date in format YYYY-MM-DD
DOCUMENT_IMPORT_FILTERS = [
    re.compile(r"\d{4}-\d{2}-\d{2}$"),
]
```

### 3. Filtering Content Within a Cell

```python
import re

# Filter rows containing "error", "warning", or "failed"
DOSSIER_IMPORT_FILTERS = [
    re.compile(r"\b(error|warning|failed)\b", re.IGNORECASE),
]

# Filter rows containing an email address
DOSSIER_IMPORT_FILTERS = [
    re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
]
```

## Important Notes

- The filtering process joins all cells in a row (with newlines replaced by spaces)
- If any pattern matches, the entire row is excluded from the output
- The original multi-line structure of cells is preserved in the Excel output

## Implementation Example

Add these filters to your `consolidate_migration_reports.py` script:

```python
import re
import sys
# ... other imports and code ...

# Define your filter patterns
DOCUMENT_EXPORT_FILTERS = [
    re.compile(r"\b(error|failed|rejected)\b", re.IGNORECASE),
]

DOCUMENT_IMPORT_FILTERS = [
    re.compile(r"^test", re.IGNORECASE),  # Rows starting with "test"
]

DOSSIER_IMPORT_FILTERS = [
    re.compile(r"\b(Aarau|Baden)\b"),
]

# ... rest of your script ...

if __name__ == "__main__":
    # ... your existing code ...
    
    # In the actual script, this would be:
    # sys.exit(main())
    pass
```

For more examples and testing functions, see the `regex_filter_examples.py` file.
