import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { findRecord } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

import hasRunningInquiriesQuery from "ember-ebau-core/gql/queries/has-running-inquiries.graphql";

/**
 * `@projectcaluma/ember-form` custom widget component to link attachments from
 * the central documents module of eBau to a caluma form.
 *
 * @class LinkAttachmentsComponent
 */
export default class LinkAttachmentsComponent extends Component {
  @service intl;
  @service notification;
  @service calumaOptions;

  @queryManager apollo;

  @tracked showModal = false;

  instance = findRecord(this, "instance", () => [this.instanceId]);

  attachmentSection = findRecord(this, "attachment-section", () => [
    this.args.field.question.raw.meta.attachmentSection,
  ]);

  hasRunningInquiries = trackedFunction(this, async () => {
    return (
      (await this.apollo.query(
        {
          query: hasRunningInquiriesQuery,
          variables: {
            currentGroupId: this.calumaOptions.currentGroupId,
            instanceId: this.instanceId,
          },
        },
        "allWorkItems.totalCount"
      )) > 0
    );
  });

  get instanceId() {
    return this.args.context.instanceId;
  }

  get isLoading() {
    return this.instance.isLoading || this.attachmentSection.isLoading;
  }

  get hasUploadPermission() {
    switch (this.attachmentSection.record?.meta["permission-name"]) {
      case "write":
      case "admin":
      case "admin-internal":
      case "admin-service":
        return true;
      case "admin-service-before-decision":
      case "admin-before-decision":
        return !this.instance.record?.isAfterDecision;
      case "admin-service-running-inquiry":
        return this.hasRunningInquiries.value;
      default:
        return false;
    }
  }

  @action
  async save(selected) {
    try {
      this.args.field.answer.value = selected;

      await this.args.field.save.perform();
    } catch (error) {
      this.notification.danger(this.intl.t("link-attachments.link-error"));
    }
  }
}
