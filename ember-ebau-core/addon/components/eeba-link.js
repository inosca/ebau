import { getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";

const eebaBaseUrl = getOwnConfig().eebaBaseUrl;

export default class EebaLinkComponent extends Component {
  get isShown() {
    return (
      this.getAnswer(
        "haben-sie-bereits-eeba-direkt-auf-eeba-onlineservice-erfasst",
      ) ===
        "haben-sie-bereits-eeba-direkt-auf-dem-eeba-onlineservice-erfasst-ja" &&
      (this.eebaId ?? "").length === 13
    );
  }

  get eebaId() {
    return this.getAnswer("eeba-id-eingeben");
  }

  getAnswer(slug) {
    try {
      return this.args.field.document.findField(slug)?.answer?.value;
    } catch (error) {
      console.error(`Error retrieving answer for slug "${slug}":`, error);
      return null;
    }
  }

  get eebaWebUrlAnswer() {
    return `${eebaBaseUrl}/web/form/${this.eebaId}/basic`;
  }
}
