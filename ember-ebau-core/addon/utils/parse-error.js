export default function parseError({ errors }, excludeFieldErrors = true) {
  if (!errors) return null;

  return errors
    .filter(
      (error) =>
        !excludeFieldErrors ||
        error.source.pointer.split("/").pop() === "non-field-errors"
    )
    .map((error) => error.detail)
    .join(", ");
}
