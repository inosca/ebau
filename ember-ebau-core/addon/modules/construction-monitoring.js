import ConstructionMonitoringController from "ember-ebau-core/controllers/construction-monitoring";
import ConstructionMonitoringConstructionStageController from "ember-ebau-core/controllers/construction-monitoring/construction-stage";
import ConstructionMonitoringConstructionStageConstructionStepController from "ember-ebau-core/controllers/construction-monitoring/construction-stage/construction-step";
import ConstructionMonitoringConstructionStageIndexController from "ember-ebau-core/controllers/construction-monitoring/construction-stage/index";
import ConstructionMonitoringIndexController from "ember-ebau-core/controllers/construction-monitoring/index";
import { registerModule } from "ember-ebau-core/modules";
import ConstructionMonitoringRoute from "ember-ebau-core/routes/construction-monitoring";
import ConstructionMonitoringConstructionStageRoute from "ember-ebau-core/routes/construction-monitoring/construction-stage";
import ConstructionMonitoringConstructionStageConstructionStepRoute from "ember-ebau-core/routes/construction-monitoring/construction-stage/construction-step";
import ConstructionMonitoringConstructionStageIndexRoute from "ember-ebau-core/routes/construction-monitoring/construction-stage/index";
import ConstructionMonitoringIndexRoute from "ember-ebau-core/routes/construction-monitoring/index";
import ConstructionMonitoringTemplate from "ember-ebau-core/templates/construction-monitoring";
import ConstructionMonitoringConstructionStageTemplate from "ember-ebau-core/templates/construction-monitoring/construction-stage";
import ConstructionMonitoringConstructionStageConstructionStepTemplate from "ember-ebau-core/templates/construction-monitoring/construction-stage/construction-step";
import ConstructionMonitoringConstructionStageIndexTemplate from "ember-ebau-core/templates/construction-monitoring/construction-stage/index";
import ConstructionMonitoringIndexTemplate from "ember-ebau-core/templates/construction-monitoring/index";

export default function register(router, options = {}) {
  router.route("construction-monitoring", options, function () {
    this.route(
      "construction-stage",
      { path: "/:construction_stage_id" },
      function () {
        this.route("construction-step", { path: "/:construction_step_id" });
      },
    );
  });

  registerModule(
    "construction-monitoring",
    router.parent,
    options.resetNamespace,
    {
      routes: {
        "construction-monitoring": ConstructionMonitoringRoute,
        "construction-monitoring/index": ConstructionMonitoringIndexRoute,
        "construction-monitoring/construction-stage":
          ConstructionMonitoringConstructionStageRoute,
        "construction-monitoring/construction-stage/construction-step":
          ConstructionMonitoringConstructionStageConstructionStepRoute,
        "construction-monitoring/construction-stage/index":
          ConstructionMonitoringConstructionStageIndexRoute,
      },
      controllers: {
        "construction-monitoring": ConstructionMonitoringController,
        "construction-monitoring/index": ConstructionMonitoringIndexController,
        "construction-monitoring/construction-stage":
          ConstructionMonitoringConstructionStageController,
        "construction-monitoring/construction-stage/construction-step":
          ConstructionMonitoringConstructionStageConstructionStepController,
        "construction-monitoring/construction-stage/index":
          ConstructionMonitoringConstructionStageIndexController,
      },
      templates: {
        "construction-monitoring": ConstructionMonitoringTemplate,
        "construction-monitoring/index": ConstructionMonitoringIndexTemplate,
        "construction-monitoring/construction-stage":
          ConstructionMonitoringConstructionStageTemplate,
        "construction-monitoring/construction-stage/construction-step":
          ConstructionMonitoringConstructionStageConstructionStepTemplate,
        "construction-monitoring/construction-stage/index":
          ConstructionMonitoringConstructionStageIndexTemplate,
      },
    },
  );
}
