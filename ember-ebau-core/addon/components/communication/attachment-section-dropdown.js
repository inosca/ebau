import { getOwner } from "@ember/application";
import { action } from "@ember/object";
import { run } from "@ember/runloop";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";
import UIkit from "uikit";

export default class CommunicationAttachmentSectionDropdownComponent extends Component {
  @service ebauModules;

  @tracked dropdownOpen = false;

  attachmentSectionsResource = query(this, "attachment-section", () => ({
    instanceId: this.args.instanceId,
  }));

  get attachmentSections() {
    const records = this.attachmentSectionsResource.records;

    if (this.args.onlySectionsForApplicant) {
      const config =
        getOwner(this).resolveRegistration("config:environment").APPLICATION
          .communication ?? {};
      const sections = config.attachmentSectionsForConversion ?? [];

      return records?.filter((attachmentSection) =>
        sections.includes(parseInt(attachmentSection.id))
      );
    }

    return records;
  }

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
