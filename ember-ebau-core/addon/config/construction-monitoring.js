import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

const STATUS_COLOR_MAP = {
  "in-progress": "default",
  completed: "success",
  "completed-muted": "muted",
  canceled: "muted",
  approved: "success",
  "not-approved": "warning",
  pending: "muted",
  unknown: "muted",
};

const STATUS_ICON_MAP = {
  "in-progress": "pencil",
  completed: "check",
  "completed-muted": "check",
  canceled: "lock",
  approved: "check",
  "not-approved": "close",
  pending: "pencil",
  unknown: "question",
};

const STATUS_LABEL_MAP = {
  "in-progress": "construction-monitoring.status.in-progress",
  completed: "construction-monitoring.status.completed",
  "completed-muted": "construction-monitoring.status.completed",
  canceled: "construction-monitoring.status.canceled",
  approved: "construction-monitoring.status.approved",
  "not-approved": "construction-monitoring.status.not-approved",
  pending: "construction-monitoring.status.pending",
  unknown: "construction-monitoring.status.pending",
};

let config;
if (macroCondition(getOwnConfig().application === "sz")) {
  config = importSync("ember-ebau-core/config/construction-monitoring-sz");
}

const sharedConfig = {
  constructionSteps: [
    "construction-step-plan-construction-stage",
    "construction-step-baufreigabe",
    "construction-step-baubeginn",
    "construction-step-kanalisationsabnahme",
    "construction-step-schnurgeruestabnahme",
    "construction-step-rohbauabnahme",
    "construction-step-zwischenkontrolle",
    "construction-step-schlussabnahme-gebaeude",
    "construction-step-schlussabnahme-projekt",
  ],
  controls: {
    initTask: "init-construction-monitoring",
    completeTask: "complete-construction-monitoring",
  },
  constructionStages: {
    constructionStageTask: "construction-stage",
  },
};

export default {
  ...sharedConfig,
  ...(config?.default ?? {}),
  STATUS_COLOR_MAP,
  STATUS_ICON_MAP,
  STATUS_LABEL_MAP,
};
