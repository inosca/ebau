import { parseBooleanFilter, parseIntegerFilter } from "./_filters";
import ApplicationSerializer from "./application";

export default class extends ApplicationSerializer {
  serialize(...args) {
    const queryParams = args[1]?.queryParams || {};
    if (!args[0]?.filter) {
      return super.serialize(...args);
    }

    const serviceParentId = parseIntegerFilter(queryParams.service_parent);
    const hasParent = parseBooleanFilter(queryParams.has_parent);

    args[0] = args[0].filter((entry) => {
      if (serviceParentId) {
        return parseInt(entry.serviceParent?.id) === serviceParentId;
      }

      if (hasParent !== undefined) {
        return true === hasParent
          ? entry.serviceParent !== null
          : entry.serviceParent === null;
      }

      return true;
    });

    return super.serialize(...args);
  }
}
