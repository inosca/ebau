import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { TrackedObject } from "tracked-built-ins";

export default class MergeMunicipalityComponent extends Component {
  @service fetch;
  @service intl;
  @service notification;
  @service store;

  adoptChildServiceOption = {
    label: this.intl.t("merge-municipality.option.adopt"),
    value: "adopt",
  };

  emptyChildServiceOption = {
    label: this.intl.t("merge-municipality.option.empty"),
    value: null,
  };

  placeholderOptions = [
    this.adoptChildServiceOption,
    this.emptyChildServiceOption,
  ];

  @tracked selectedMunicipalityFrom = null;
  @tracked selectedMunicipalityTo = null;
  @tracked selectedChildServices = new TrackedObject({});

  @tracked municipalities = [];
  @tracked childServicesFrom = [];
  @tracked childServicesTo = [];

  @tracked mergeResult = {};

  @tracked migrationCompleted = false;
  @tracked showPreviewButton = false;
  @tracked showResult = false;

  constructor(...args) {
    super(...args);
    this.loadMunicipalities();
  }

  @action async selectMunicipality(input, value) {
    this.resetCommon();

    if ("from" === input) {
      this.selectedMunicipalityTo = null;
      this.selectedMunicipalityFrom = value;
    } else {
      if (this.selectedMunicipalityFrom?.value === value.value) {
        this.selectedMunicipalityTo = null;
        return;
      }

      this.selectedMunicipalityTo = value;
    }

    if (this.selectedMunicipalityFrom && this.selectedMunicipalityTo) {
      await this.loadChildServices("from", this.selectedMunicipalityFrom.value);
      await this.loadChildServices("to", this.selectedMunicipalityTo.value);

      this.selectedChildServices = new TrackedObject(
        this.childServicesFrom.reduce((acc, v) => {
          acc[v.value] = this.emptyChildServiceOption;
          return acc;
        }, {}),
      );

      this.updateResult();
    }
  }

  @action selectChildService(childServiceFrom, childServiceTo) {
    if (!childServiceFrom?.value) {
      return;
    }

    if (!childServiceTo?.value) {
      childServiceTo = this.emptyChildServiceOption;
    }

    this.selectedChildServices[childServiceFrom.value] = childServiceTo;
    this.updateResult();
  }

  @action submitPreview() {
    if (this.showResult) {
      return;
    }

    this.showPreviewButton = false;
    this.showResult = true;
  }

  @action resetMerge() {
    this.selectedMunicipalityFrom = null;
    this.selectedMunicipalityTo = null;
    this.resetCommon();
  }

  @action cancel() {
    this.showPreviewButton = true;
    this.showResult = false;
  }

  @dropTask
  *confirm() {
    yield this.performConfirm();
  }

  async performConfirm() {
    if (
      !(await confirm(this.intl.t("merge-municipality.result.confirm-dialog")))
    ) {
      return;
    }

    const mapping = this.mergeResult
      .map((v) => {
        if (v.action === "retain") {
          return false;
        }

        return {
          from_service: parseInt(v.from.value),
          to_service: parseInt(v.action === "adopt" ? null : v.to.value),
          action: v.action,
        };
      })
      .filter(Boolean);

    await this.fetch
      .fetch("/api/v1/services/merge-municipality", {
        method: "POST",
        body: JSON.stringify({
          data: {
            type: "services",
            attributes: {
              from_municipality: parseInt(this.selectedMunicipalityFrom.value),
              to_municipality: parseInt(this.selectedMunicipalityTo.value),
              mapping,
            },
          },
        }),
      })
      .then(() => {
        this.migrationCompleted = true;
      })
      .catch(() => {
        this.notification.danger(
          this.intl.t("merge-municipality.result.error"),
        );
      });
  }

  async loadMunicipalities() {
    this.municipalities = (
      await this.store.query("public-service", {
        service_group_name: "municipality",
        has_parent: false,
      })
    ).map((v) => ({ label: v.name, value: v.id }));
  }

  async loadChildServices(input, serviceId) {
    const childServices = (
      await this.store.query("public-service", {
        service_parent: serviceId,
      })
    ).map((v) => ({ label: v.name, value: v.id }));

    if ("from" === input) {
      this.childServicesFrom = childServices;
    } else {
      childServices.unshift(this.adoptChildServiceOption);
      childServices.unshift(this.emptyChildServiceOption);
      this.childServicesTo = childServices;
    }
  }

  resetCommon() {
    this.childServicesFrom = [];
    this.childServicesTo = [];
    this.selectedChildServices = new TrackedObject({});
    this.mergeResult = {};
    this.showPreviewButton = false;
    this.showResult = false;
    this.migrationCompleted = false;
  }

  updateResult() {
    this.showPreviewButton = false;
    this.showResult = false;

    let hasMissingEntry = false;
    const result = {};
    for (const selection of Object.entries(this.selectedChildServices)) {
      const [fromId, to] = selection;
      const from = this.childServicesFrom.find((s) => s.value === fromId);
      if (!from) {
        continue;
      }

      let action;
      if (to.value === this.emptyChildServiceOption.value) {
        hasMissingEntry = true;
        continue;
      } else if (to.value === this.adoptChildServiceOption.value) {
        action = "adopt";
      } else {
        action = "merge";
      }

      result[fromId] = {
        to,
        from,
        action,
      };
    }

    // add retained services to result
    const mappedIds = Object.values(this.selectedChildServices)
      .filter((v) => !this.placeholderOptions.includes(v))
      .map((v) => v.value);

    for (const toEntry of this.childServicesTo) {
      if (
        toEntry.value === this.emptyChildServiceOption.value ||
        toEntry.value === this.adoptChildServiceOption.value ||
        mappedIds.includes(toEntry.value)
      ) {
        continue;
      }

      if (typeof result[toEntry.value] === "undefined") {
        result[toEntry.value] = {
          from: toEntry,
          to: toEntry,
          action: "retain",
        };
      }
    }

    const actionSort = ["merge", "retain", "adopt"];
    this.mergeResult = Object.values(result).sort((a, b) => {
      return (
        actionSort.indexOf(a.action) - actionSort.indexOf(b.action) ||
        a.from.label.localeCompare(b.from.label)
      );
    });

    this.showPreviewButton = !hasMissingEntry;
  }

  getMergeActionTranslationForEntry = (resultEntry) => {
    const action = resultEntry?.action || "none";

    return this.intl.t(`merge-municipality.result.action.${action}`);
  };

  getMergeActionIconForEntry = (resultEntry) => {
    const action = resultEntry?.action || "none";

    if ("merge" === action) {
      return "icon: chevron-right";
    } else if ("adopt" === action) {
      return "icon: plus";
    }
    return "icon: lock";
  };
}
