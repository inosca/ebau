export default {
  exportTypes: {
    byRoles: {
      municipality: ["dossiers-municipality"],
      service: ["dossiers-service", "work-items"],
    },
    byServiceGroups: {
      "service-afb": ["dossiers-service", "work-items"],
      "cantonal-service": ["dossiers-service", "work-items"],
    },
  },
};
