import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import slugify from "@projectcaluma/ember-core/utils/slugify";
import { dropTask } from "ember-concurrency";
import saveAs from "file-saver";
import QRCode from "qrcode";

export default class QrCodeComponent extends Component {
  @service notifications;
  @service shoebox;
  @service intl;

  @tracked data;

  constructor(...args) {
    super(...args);

    this.initQRCode();
  }

  async initQRCode() {
    this.data = await QRCode.toDataURL(this.url, { quality: 1 });
  }

  get key() {
    return this.args.field.document.uuid.substr(0, 7);
  }

  get url() {
    const host = this.shoebox.content?.config?.portalURL;
    const id = this.args.context.instanceId;

    return `${host}/public-instances/${id}?key=${this.key}`;
  }

  @dropTask
  *download(e) {
    e.preventDefault();

    try {
      const blob = yield (yield fetch(this.data)).blob();
      const form = this.args.field.document.rootForm.name;

      yield saveAs(
        blob,
        `${this.args.context.instanceId}-${slugify(form)}-qr-code.png`
      );
    } catch (error) {
      this.notifications.error(this.intl.t("qr-code.downloadError"));
    }
  }
}
