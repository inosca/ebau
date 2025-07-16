import { importSync, getOwnConfig, macroCondition } from "@embroider/macros";

let config;
if (macroCondition(getOwnConfig().application === "ur")) {
  config = importSync("ember-ebau-core/config/additional-demands-ur");
} else if (macroCondition(getOwnConfig().application === "be")) {
  config = importSync("ember-ebau-core/config/additional-demands-be");
}

const sharedConfig = {
  STATUS_ICON_MAP: {
    internal: {
      draft: "commenting",
      sent: "file-edit",
      "needs-interaction": "file-text",
      completed: "check",
      canceled: "close",
    },
    portal: {
      sent: "comment",
      "needs-interaction": "file-text",
      completed: "check",
      canceled: "close",
    },
  },
  STATUS_COLOR_MAP: {
    internal: {
      draft: "default",
      sent: "default",
      "needs-interaction": "default",
      completed: "default",
      canceled: "default",
    },
    portal: {
      sent: "default",
      "needs-interaction": "default",
      completed: "default",
      canceled: "default",
    },
  },
};

export default {
  ...sharedConfig,
  ...(config?.default ?? {}),
};
