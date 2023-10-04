import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";

export default class DetailController extends Controller {
  @service router;
  @service store;

  // only fetch the case as the instance is already fetched in the route
  cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model.id }],
      },
    ],
  }));

  get useFullScreen() {
    return (
      this.router.isActive("cases.detail.alexandria") ||
      this.router.isActive("communications")
    );
  }

  get case() {
    return this.cases.value?.[0];
  }
}
