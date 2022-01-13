import { helper } from "@ember/component/helper";

export default helper(function isEmbedded() {
  return window.frameElement !== null;
});
