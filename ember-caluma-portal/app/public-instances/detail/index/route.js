import Route from "@ember/routing/route";

import { hasFeature } from "caluma-portal/helpers/has-feature";

export default class PublicInstancesDetailIndexRoute extends Route {
  redirect() {
    const redirectTo = hasFeature("publication.form")
      ? "public-instances.detail.form"
      : "public-instances.detail.documents";

    this.replaceWith(redirectTo);
  }
}
