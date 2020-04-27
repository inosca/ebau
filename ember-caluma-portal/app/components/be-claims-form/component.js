import { getOwner } from "@ember/application";
import EmberObject, { action } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import CfFormComponent from "ember-caluma/components/cf-form";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

function field(fieldName) {
  return function() {
    return {
      get() {
        return this.document.findField(fieldName);
      }
    };
  };
}

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

  get isAnswered() {
    return [
      "nfd-tabelle-status-beantwortet",
      "nfd-tabelle-status-erledigt"
    ].includes(this.statusSlug);
  }

  get deadlineDate() {
    return moment(this.deadline.answer.value);
  }

  get answeredDate() {
    return moment(this.answered.answer.value);
  }

  get isOverdue() {
    return moment(this.deadlineDate) < moment();
  }

  get service() {
    return this.store.peekRecord("public-service", this.authority.answer.value);
  }
}

export default class BeClaimsFormComponent extends CfFormComponent {
  @service intl;
  @service store;

  @tracked activeClaimType = "pending";

  get claimTypes() {
    return ["pending", "answered"];
  }

  get allClaims() {
    const table = this.fieldset.document.findField("nfd-tabelle-table");

    return table.answer.value.map(document => {
      return Claim.create(getOwner(this).ownerInjection(), { document });
    });
  }

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
  *fetchServices() {
    yield this.store.query("public-service", {
      service_id: [
        ...new Set(this.allClaims.map(claim => claim.authority.answer.value))
      ].join(",")
    });
  }

  @action
  setEditedClaim(claim, event) {
    if (event) event.preventDefault();

    this.set("editedClaim", claim);
  }
}
