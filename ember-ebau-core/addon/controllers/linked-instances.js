import Controller from "@ember/controller";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";

export default class LinkedInstancesController extends Controller {
  // only fetch the case as the instance is already fetched in the route
  cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model.id }],
      },
    ],
  }));

  get case() {
    return this.cases.value?.[0];
  }
}
