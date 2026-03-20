import { service } from "@ember/service";
import CalumaOptionsService from "@projectcaluma/ember-core/services/caluma-options";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import fetchIfNotCached from "ember-ebau-core/utils/fetch-if-not-cached";

export default class CustomCalumaOptionsService extends CalumaOptionsService {
  @service store;

  useNumberSeparatorWidgetAsDefault = hasFeature(
    "caluma.useNumberSeparatorWidgetAsDefault",
  );

  resolveUsers(identifiers) {
    return fetchIfNotCached("public-user", "username", identifiers, this.store);
  }

  resolveGroups(identifiers) {
    return fetchIfNotCached(
      "public-service",
      "service_id",
      identifiers,
      this.store,
    );
  }
}
