import { helper } from "@ember/component/helper";

function addThousandSeparator(number) {
  return number
    .toLocaleString("en-US", { maximumFractionDigits: 0 })
    .replaceAll(",", "'");
}

export default helper(function formatCoordinate([coordinate]) {
  if (!coordinate) {
    return "";
  }
  const x = addThousandSeparator(coordinate.x);
  const y = addThousandSeparator(coordinate.y);

  return `${x} / ${y}`;
});
