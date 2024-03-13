import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask, enqueueTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class SnippetsComponent extends Component {
  @service fetch;
  @service store;
  @service calumaOptions;

  _inputElement = null;

  snippets = trackedTask(this, this.fetchSnippets, () => [
    this.calumaOptions.currentServiceId,
  ]);

  @dropTask
  *fetchSnippets(serviceId) {
    let snippets = this.store
      .peekAll("notification-template")
      .filter((template) => {
        return (
          parseInt(template.belongsTo("service").id()) === serviceId &&
          template.notificationType === "textcomponent"
        );
      });

    if (!snippets.length) {
      snippets = yield this.store.query("notification-template", {
        service: serviceId,
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

  @enqueueTask
  *applySnippet(id, event) {
    event.preventDefault();

    const response = yield this.fetch.fetch(
      `/api/v1/notification-templates/${id}/merge?instance=${this.calumaOptions.currentInstanceId}`,
    );

    const { data } = yield response.json();

    this._inputElement.value = this._inputElement.value + data.attributes.body;
    this._inputElement.dispatchEvent(new Event("input"));
  }

  @action
  registerInputElement(element) {
    this._inputElement =
      element.querySelector("textarea") ?? element.querySelector("input");
  }
}
