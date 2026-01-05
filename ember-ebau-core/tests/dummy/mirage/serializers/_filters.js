export function parseBooleanFilter(value) {
  if ([false, "false", true, "true"].includes(value)) {
    return value === "true" || value === true;
  }

  return undefined;
}

export function parseIntegerFilter(value) {
  return parseInt(value);
}
