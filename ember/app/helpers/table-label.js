import { helper } from "@ember/component/helper";

export function tableLabel([column]) {
  return column["table-label"] || column.label;
}

export default helper(tableLabel);
