import { helper } from "@ember/component/helper";

export default helper(function round([number]) {
  if (!number) {
    return "";
  }

  return Math.round(number);
});
