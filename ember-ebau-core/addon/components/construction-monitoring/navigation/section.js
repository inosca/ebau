import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class ConstructionMonitoringNavigationSectionComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;
  @service constructionMonitoring;

  @tracked expanded;

  constructor(...args) {
    super(...args);
    this.expanded =
      this.args.constructionStage.childCase.status === "RUNNING" ||
      this.isActive;
  }

  get isActive() {
    return this.router.isActive(
      this.ebauModules.resolveModuleRoute(
        "construction-monitoring",
        "construction-stage",
      ),
      decodeId(this.args.constructionStage.id),
    );
  }

  get status() {
    return this.constructionMonitoring.constructionStageStatus(
      this.args.constructionStage,
    );
  }

  @action
  toggle(e) {
    e.preventDefault();

    this.expanded = !this.expanded;
  }
}
