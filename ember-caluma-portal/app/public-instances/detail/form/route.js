import Route from "@ember/routing/route";

import { hasFeature } from "caluma-portal/helpers/has-feature";

export default class PublicInstancesDetailFormRoute extends Route {
  redirectTo() {
    if (!hasFeature("publication.form")) {
      return this.replaceWith("public-instances.detail.index");
    }
  }
}
