import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class SnippetAbility extends Ability {
  @service ebauModules;

  #isEditable(snippet) {
    if (snippet.service.id === null) {
      return (
        hasFeature("snippets.allowGlobalSnippets") &&
        this.ebauModules.isSupportRole
      );
    }

    return snippet.service.id === String(this.ebauModules.serviceId);
  }

  get canView() {
    if (this.type === "system") {
      return hasFeature("snippets.allowGlobalSnippets");
    }

    // Support doesn't see any service specific snippets
    return !this.ebauModules.isSupportRole;
  }

  get canEditCategory() {
    return this.snippets.every((snippet) => this.#isEditable(snippet));
  }

  get canEdit() {
    return this.#isEditable(this.model);
  }

  get canAdd() {
    if (this.type === "system") {
      return (
        hasFeature("snippets.allowGlobalSnippets") &&
        this.ebauModules.isSupportRole
      );
    }

    return !this.ebauModules.isSupportRole;
  }
}
