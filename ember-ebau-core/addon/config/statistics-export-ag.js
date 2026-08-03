export default {
  exportTypes: {
    byRoles: {
      municipality: ["dossiers-municipality"],
      service: ["dossiers-service", "work-items"],
    },
    byServiceGroups: {
      "service-afb": ["dossiers-service", "work-items", "rpg2"],
      "cantonal-service": ["dossiers-service", "work-items"],
    },
  },
};
