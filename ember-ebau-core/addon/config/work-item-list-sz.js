export default {
  showTaskFilter: true,
  availableTasks: {
    roles: {
      municipality: ["complete-check", "init-distribution", "make-decision"],
      service: ["fill-inquiry", "inquiry", "check-inquiry", "alter-inquiry"],
    },
    services: {
      /* Baugesuchszentrale (Fachstelle) */
      7: ["check-inquiries"],
    },
    default: [],
  },
};
