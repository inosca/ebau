import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { enqueueTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { groupAndSort } from "ember-ebau-core/utils/snippets";

export default class SnippetsComponent extends Component {
  @service fetch;
  @service store;
  @service calumaOptions;

  _inputElement = null;

  snippets = trackedFunction(this, async () => {
    const currentServiceId = this.calumaOptions.currentGroupId;
    const globalSnippetsEnabled = hasFeature("snippets.allowGlobalSnippets");

    let snippets = this.store
      .peekAll("notification-template")
      .filter((template) => {
        const serviceId = template.belongsTo("service").id();
        const isValidService =
          serviceId !== null
            ? serviceId === currentServiceId
            : globalSnippetsEnabled;

        return template.notificationType === "textcomponent" && isValidService;
      });

    if (!snippets.length) {
      snippets = await this.store.query("notification-template", {
        service: !globalSnippetsEnabled ? currentServiceId : undefined,
        type: "textcomponent",
      });
    }

    const ownSnippets = [];
    const systemSnippets = [];

    snippets.forEach((snippet) => {
      const snippetServiceId = snippet.belongsTo("service").id();

      if (snippetServiceId !== null && snippetServiceId === currentServiceId) {
        ownSnippets.push(snippet);
      } else if (globalSnippetsEnabled) {
        systemSnippets.push(snippet);
      }
    });

    const data = {
      own: groupAndSort(ownSnippets),
    };

    if (globalSnippetsEnabled) {
      data.system = groupAndSort(systemSnippets);
    }
    return data;
  });

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
