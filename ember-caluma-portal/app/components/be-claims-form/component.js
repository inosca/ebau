import { getOwner, setOwner } from "@ember/application";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import moment from "moment";

function field(fieldName) {
  return function () {
    return {
      get() {
        return this.document.findField(fieldName);
      },
    };
  };
}

class Claim {
  @service store;

  constructor(document) {
    this.document = document;
  }

  @field("nfd-tabelle-status") status;
  @field("nfd-tabelle-beschreibung") description;
  @field("nfd-tabelle-bemerkung") comment;
  @field("nfd-tabelle-frist") deadline;
  @field("nfd-tabelle-datum-antwort") answered;
  @field("nfd-tabelle-behoerde") authority;

  get id() {
    return this.document.id;
  }

  get statusSlug() {
    return this.status.answer.value;
  }

  get isAnswered() {
    return [
      "nfd-tabelle-status-beantwortet",
      "nfd-tabelle-status-erledigt",
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

export default class BeClaimsFormComponent extends Component {
  @service intl;
  @service store;

  @tracked activeClaimType = "pending";
  @tracked editedClaim;

  get claimTypes() {
    return ["pending", "answered"];
  }

  get allClaims() {
    const table = this.args.fieldset.document.findField("nfd-tabelle-table");

    return table.answer.value.map((document) => {
      const claim = new Claim(document);
      setOwner(claim, getOwner(this));
      return claim;
    });
  }

  get claims() {
    return {
      pending: this.allClaims.filter((claim) =>
        ["nfd-tabelle-status-in-bearbeitung"].includes(claim.statusSlug)
      ),
      answered: this.allClaims.filter((claim) =>
        [
          "nfd-tabelle-status-beantwortet",
          "nfd-tabelle-status-erledigt",
        ].includes(claim.statusSlug)
      ),
    };
  }

  @dropTask
  *fetchServices() {
    yield this.store.query("public-service", {
      service_id: [
        ...new Set(this.allClaims.map((claim) => claim.authority.answer.value)),
      ].join(","),
    });
  }

  @action
  setEditedClaim(claim, event) {
    if (event) event.preventDefault();

    this.editedClaim = claim;
  }
}
