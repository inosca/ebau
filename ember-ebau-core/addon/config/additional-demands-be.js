export default {
  buckets: [
    "dokument-grundstucksangaben",
    "dokument-gutachten-nachweise-begrundungen",
    "dokument-projektplane-projektbeschrieb",
    "dokument-weitere-gesuchsunterlagen",
  ],
  section: "7",
  sectionPaper: "12",
  STATUS_COLOR_MAP: {
    internal: {
      draft: "muted",
      sent: "default",
      "needs-interaction": "warning",
      completed: "success",
      canceled: "muted",
    },
    portal: {
      sent: "warning",
      "needs-interaction": "muted",
      completed: "success",
      canceled: "muted",
    },
  },
};
