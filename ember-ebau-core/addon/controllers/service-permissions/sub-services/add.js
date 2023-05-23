import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class ServicePermissionsSubServicesIndexController extends Controller {
  @service intl;

  get warning() {
    return this.intl.t("service-permissions.sub-services-add-warning", {
      htmlSafe: true,
    });
  }
}
