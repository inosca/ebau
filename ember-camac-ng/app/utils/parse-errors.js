export default function parseErrors(errors) {
  return errors.map((error) => error.detail).join(", ");
}
