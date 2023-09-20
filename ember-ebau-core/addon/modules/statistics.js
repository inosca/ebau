import StatisticsAvgCycleTimeController from "ember-ebau-core/controllers/statistics/avg-cycle-time";
import StatisticsCycleTimeController from "ember-ebau-core/controllers/statistics/cycle-time";
import StatisticsIndexContoller from "ember-ebau-core/controllers/statistics/index";
import StatisticsProcessTimeController from "ember-ebau-core/controllers/statistics/process-time";
import { registerModule } from "ember-ebau-core/modules";
import StatisticsRoute from "ember-ebau-core/routes/statistics";
import StatisticsAvgCycleTimeRoute from "ember-ebau-core/routes/statistics/avg-cycle-time";
import StatisticsCycleTimeRoute from "ember-ebau-core/routes/statistics/cycle-time";
import StatisticsIndexRoute from "ember-ebau-core/routes/statistics/index";
import StatisticsProcessTimeRoute from "ember-ebau-core/routes/statistics/process-time";
import StatisticsTemplate from "ember-ebau-core/templates/statistics";
import StatisticsAvgCycleTimeTemplate from "ember-ebau-core/templates/statistics/avg-cycle-time";
import StatisticsCycleTimeTemplate from "ember-ebau-core/templates/statistics/cycle-time";
import StatisticsIndexTemplate from "ember-ebau-core/templates/statistics/index";
import StatisticsProcessTimeTemplate from "ember-ebau-core/templates/statistics/process-time";

export default function register(router, options = {}) {
  router.route("statistics", options, function () {
    this.route("avg-cycle-time");
    this.route("cycle-time");
    this.route("process-time");
  });

  registerModule("statistics", router.parent, options.resetNamespace, {
    routes: {
      statistics: StatisticsRoute,
      "statistics/index": StatisticsIndexRoute,
      "statistics/avg-cycle-time": StatisticsAvgCycleTimeRoute,
      "statistics/cycle-time": StatisticsCycleTimeRoute,
      "statistics/process-time": StatisticsProcessTimeRoute,
    },
    controllers: {
      "statistics/index": StatisticsIndexContoller,
      "statistics/avg-cycle-time": StatisticsAvgCycleTimeController,
      "statistics/cycle-time": StatisticsCycleTimeController,
      "statistics/process-time": StatisticsProcessTimeController,
    },
    templates: {
      statistics: StatisticsTemplate,
      "statistics/index": StatisticsIndexTemplate,
      "statistics/avg-cycle-time": StatisticsAvgCycleTimeTemplate,
      "statistics/cycle-time": StatisticsCycleTimeTemplate,
      "statistics/process-time": StatisticsProcessTimeTemplate,
    },
  });
}
