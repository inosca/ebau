export default function parseError({ errors }) {
  if (!errors) return null;

  return errors
    .filter(
      (error) => error.source.pointer.split("/").pop() === "non-field-errors"
    )
    .map((error) => error.detail)
    .join(", ");
}
