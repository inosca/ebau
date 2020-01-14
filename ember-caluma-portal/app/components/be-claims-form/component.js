import { getOwner } from "@ember/application";
import EmberObject, { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import config from "ember-caluma-portal/config/environment";
import CfFormComponent from "ember-caluma/components/cf-form";
import { dropTask } from "ember-concurrency-decorators";
import gql from "graphql-tag";
import moment from "moment";

const field = fieldName =>
  computed("document", function() {
    return this.document.findField(fieldName);
  });

class Claim extends EmberObject {
  @service store;

  @reads("document.uuid") id;
  @reads("status.answer.value") statusSlug;

  @field("nfd-tabelle-status") status;
  @field("nfd-tabelle-beschreibung") description;
  @field("nfd-tabelle-bemerkung") comment;
  @field("nfd-tabelle-frist") deadline;
  @field("nfd-tabelle-datum-antwort") answered;
  @field("nfd-tabelle-behoerde") authority;

  @computed("statusSlug")
  get isAnswered() {
    return [
      "nfd-tabelle-status-beantwortet",
      "nfd-tabelle-status-erledigt"
    ].includes(this.statusSlug);
  }

  @computed("deadline.answer.value")
  get deadlineDate() {
    return moment(this.deadline.answer.value);
  }

  @computed("answered.answer.value")
  get answeredDate() {
    return moment(this.answered.answer.value);
  }

  @computed("deadlineDate")
  get isOverdue() {
    return moment(this.deadlineDate) < moment();
  }

  @computed("authority.answer.value")
  get service() {
    return this.store.peekRecord("public-service", this.authority.answer.value);
  }

  @computed("id")
  get attachments() {
    return this.store
      .peekAll("attachment")
      .filter(attachment => attachment.get("context.claimId") === this.id);
  }
}

export default class BeClaimsFormComponent extends CfFormComponent {
  @service intl;
  @service store;

  @queryManager apollo;

  init(...args) {
    super.init(...args);

    this.setProperties({
      claimTypes: ["pending", "answered"],
      activeClaimType: "pending"
    });

    this.fetchTags.perform();
    this.fetchAttachments.perform();
    this.fetchServices.perform();
  }

  @computed
  get allClaims() {
    const table = this.fieldset.document.findField("nfd-tabelle-table");

    return table.answer.value.map(document => {
      return Claim.create(getOwner(this).ownerInjection(), { document });
    });
  }

  @computed("allClaims.@each.statusSlug")
  get claims() {
    return {
      pending: this.allClaims.filter(claim =>
        ["nfd-tabelle-status-in-bearbeitung"].includes(claim.statusSlug)
      ),
      answered: this.allClaims.filter(claim =>
        [
          "nfd-tabelle-status-beantwortet",
          "nfd-tabelle-status-erledigt"
        ].includes(claim.statusSlug)
      )
    };
  }

  @dropTask
  *fetchAttachments() {
    yield this.store.query("attachment", {
      instance: this.context.instanceId,
      attachment_sections: config.ebau.claims.attachmentSectionId
    });
  }

  @dropTask
  *fetchServices() {
    yield this.store.query("public-service", {
      service_id: [
        ...new Set(this.allClaims.map(claim => claim.authority.answer.value))
      ].join(",")
    });

    this.allClaims.forEach(claim => claim.notifyPropertyChange("service"));
  }

  @computed("fetchTags.lastSuccessful.value", "intl.locale")
  get tags() {
    const raw = this.getWithDefault("fetchTags.lastSuccessful.value", []);

    return raw.reduce((grouped, tag) => {
      const category = this.intl.t(
        `documents.tags.${tag.meta.documentCategory}`
      );

      let group = grouped.find(g => g.groupName === category);

      if (!group) {
        group = {
          groupName: category,
          options: []
        };

        grouped.push(group);
      }

      group.options.push(tag);

      return grouped;
    }, []);
  }

  @dropTask
  *fetchTags() {
    const raw = yield this.apollo.query(
      {
        query: gql`
          query {
            allQuestions(metaHasKey: "documentCategory") {
              edges {
                node {
                  slug
                  label
                  meta
                }
              }
            }
          }
        `
      },
      "allQuestions.edges"
    );

    return raw.map(({ node }) => node);
  }
}
