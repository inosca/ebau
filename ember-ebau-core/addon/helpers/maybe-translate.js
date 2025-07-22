import Helper from "@ember/component/helper";
import { service } from "@ember/service";

/**
 * A helper that attempts to translate a given string and returns a fallback if the translation is not found.
 *
 * @class MaybeTranslate
 * @extends {Helper}
 */
export default class MaybeTranslate extends Helper {
  @service intl;

  compute([translationLookupString, fallbackString = ""], intlKeywordArgs) {
    return this.intl.exists(translationLookupString)
      ? this.intl.t(translationLookupString, intlKeywordArgs)
      : fallbackString;
  }
}
