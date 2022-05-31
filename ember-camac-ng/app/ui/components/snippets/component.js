import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class SnippetsComponent extends Component {
  @service fetch;
  @service store;
  @service shoebox;

  snippets = trackedTask(this, this.fetchSnippets, () => [
    this.shoebox.content.serviceId,
  ]);

  @dropTask
  *fetchSnippets() {
    let snippets = this.store
      .peekAll("notification-template")
      .filter((template) => {
        return (
          parseInt(template.belongsTo("service").id()) ===
            this.shoebox.content.serviceId &&
          template.notificationType === "textcomponent"
        );
      });

    if (!snippets.length) {
      snippets = yield this.store.query("notification-template", {
        service: this.shoebox.content.serviceId,
        type: "textcomponent",
      });
    }

    return snippets.reduce((categorized, snippet) => {
      if (!(snippet.purpose in categorized)) {
        categorized[snippet.purpose] = [];
      }

      categorized[snippet.purpose].push(snippet);

      return categorized;
    }, {});
  }

  @dropTask
  *applySnippet(id, event) {
    event.preventDefault();

    const response = yield this.fetch.fetch(
      `/api/v1/notification-templates/${id}/merge?instance=${this.shoebox.content.instanceId}`
    );

    const { data } = yield response.json();

    this.args.onApply(data.attributes.body);
  }
}
