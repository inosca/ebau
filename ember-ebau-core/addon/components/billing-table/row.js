import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";

export default class BillingTableRowComponent extends Component {
  @service intl;
  @service abilities;
  @service notification;

  @action
  toggle() {
    this.args.onToggle(this.args.entry.id);
  }

  delete = dropTask(this, async () => {
    if (
      this.abilities.cannot("delete billing-v2-entry", this.args.entry) ||
      !(await confirm(this.intl.t("billing.confirm-delete")))
    ) {
      return;
    }

    // We must use `.then()` / `.catch()` here because this component will be
    // destroyed when the response of the deletion is returned as `store.query`
    // removes the destroyed object instantly. However, the hard refresh of the
    // query is necessary because we need to recalculate the totals.
    this.args.entry
      .destroyRecord()
      .then(() => this.args.onRefresh())
      .catch(() =>
        this.notification.danger(this.intl.t("billing.delete-error")),
      );
  });
}
