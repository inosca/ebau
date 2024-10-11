import Helper from "@ember/component/helper";

export default class TruncateTextHelper extends Helper {
  compute([str, limit = 200]) {
    if (str.length <= limit) return str;

    const lastSpaceIndex = str.lastIndexOf(" ", limit);
    const cutoff = lastSpaceIndex > -1 ? lastSpaceIndex : limit;
    return `${str.slice(0, cutoff)}...`;
  }
}
