import { helper } from "@ember/component/helper";

export function isEmbedded() {
  return window.top !== window;
}

export default helper(isEmbedded);
