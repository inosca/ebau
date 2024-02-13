import { action } from "@ember/object";
import { run } from "@ember/runloop";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "ember-resources/util/function";
import UIkit from "uikit";

import mainConfig from "ember-ebau-core/config/main";

export default class CommunicationAttachmentSectionDropdownComponent extends Component {
  @service store;
  @service ebauModules;

  @tracked dropdownOpen = false;

  attachmentSections = trackedFunction(this, async () => {
    await Promise.resolve();

    const sections =
      mainConfig.documentBackend === "camac"
        ? await this.store.query("attachment-section", {
            instance: this.args.instanceId,
          })
        : await this.store.query("category", {
            filter: { hasParent: false },
            include: "children",
          });

    if (!this.args.onlyWithUploadPermission) {
      return sections;
    }

    return (
      await Promise.all(
        sections.map(async (section) => {
          const canUpload = await section.canUpload(
            this.args.instanceId,
            this.ebauModules.serviceId,
          );

          return canUpload ? section : null;
        }),
      )
    ).filter(Boolean);
  });

  @action
  selectSection(attachmentSection, event) {
    event.preventDefault();
    UIkit.dropdown(event.target.closest("div[uk-dropdown]")).hide(0);
    this.args.selectSection(attachmentSection);
  }

  @action
  setupDropdown(dropdown) {
    UIkit.util.on(dropdown, "beforeshow", () => {
      run(() => (this.dropdownOpen = true));
    });
    UIkit.util.on(dropdown, "hide", () => {
      run(() => (this.dropdownOpen = false));
    });
  }
}
