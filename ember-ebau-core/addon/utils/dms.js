export const MIME_TYPE_TO_ENGINE = {
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
    "xlsx-template",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    "docx-template",
};

export const MIME_TYPE_TO_EXTENSION = {
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    ".docx",
};

export function sortByDescription(a, b) {
  return a.description.localeCompare(b.description);
}
