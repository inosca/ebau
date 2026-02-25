# Migration Report Consolidation Script

This script consolidates CSV files from migration report directories into Excel files. Each Excel file contains worksheets for different report types (document_export, document_import, dossier_import) and combines data from multiple CSV files.

## Key Features

- Processes multiple migration directories in chronological order (oldest first)
- Handles different sets of municipalities per segment
- Creates Excel files with worksheets for each report type
- Applies filters based on chronological order
- Preserves multi-line cells in Excel output
- Supports both absolute and relative paths for input and output directories

## How the Script Handles Different Municipalities per Segment

The script is designed to handle the case where different segments contain different sets of municipalities:

1. For each segment, it collects all municipalities found across all report types (document_export, document_import, dossier_import)
2. Each segment is processed independently, creating its own set of Excel files
3. Excel files are only created for municipalities that exist in a particular segment
4. Within each segment's Excel file, worksheets are created for all report types, even if a municipality doesn't have data for all report types

This approach ensures that:
- Each segment directory contains Excel files only for municipalities present in that segment
- No empty Excel files are created for municipalities that don't exist in a segment
- The script correctly handles the case where different segments have different sets of municipalities

## Directory Naming and Chronological Processing

The script processes input directories in chronological order based on timestamps in directory names. Directory names should follow this format:

```
yyyy-mm-dd_HH-MM-SS_env[_suffix]
```

For example: `2025-11-10_10-00-00_prod_nachmigration2`

Directories with valid timestamps are processed first (oldest to newest), followed by directories without timestamps in their original order.

## Chronological Filter Application

The script applies filters based on chronological order and report type using two sets of filters for each report type:

- **First-time filters**: Applied only to the oldest chronological migration source directory
  - FIRST_TIME_DOCUMENT_EXPORT_FILTERS for document_export reports
  - FIRST_TIME_DOCUMENT_IMPORT_FILTERS for document_import reports
  - FIRST_TIME_DOSSIER_IMPORT_FILTERS for dossier_import reports

- **Always filters**: Applied to all migration source directories
  - ALWAYS_DOCUMENT_EXPORT_FILTERS for document_export reports
  - ALWAYS_DOCUMENT_IMPORT_FILTERS for document_import reports
  - ALWAYS_DOSSIER_IMPORT_FILTERS for dossier_import reports

The filtering logic works as follows:

- For the oldest import directory (chronologically): Both first-time and always filters are applied
  - This ensures the most thorough filtering is applied to the oldest data

- For other directories: Only always filters are applied
  - This allows consistent filtering across all directories for certain patterns
  
- If no always filters are defined for a report type, no filtering is applied to non-oldest directories

This approach provides flexibility to filter certain patterns only in the oldest data (using first-time filters) while consistently filtering other patterns across all data (using always filters).

## Usage

```
python consolidate_migration_reports.py INPUT_PATH1 [INPUT_PATH2 ...] -o OUTPUT_DIR
```

Examples:

Process a single migration directory:
```
python consolidate_migration_reports.py /path/to/migration -o /path/to/output
```

Process multiple migration directories (filters applied based on chronological order):
```
python consolidate_migration_reports.py /path/to/migration1 /path/to/migration2 /path/to/migration3 -o /path/to/output
```

In the second example, if the directories are named with timestamps:
- The chronologically oldest directory will have both first-time and always filters applied
- Other directories will have only always filters applied
- If no always filters are defined for a report type, no filtering is applied to non-oldest directories
