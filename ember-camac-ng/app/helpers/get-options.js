import { helper } from "@ember/component/helper";

export default helper(function getOptions([obj, key]) {
  return obj[key]?.records ?? obj[key]?.value ?? obj[key] ?? [];
});
