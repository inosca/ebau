import Controller from "@ember/controller";

import config from "ember-caluma-portal/config/environment";

const { environment } = config;

export default class ApplicationController extends Controller {
  queryParams = ["language", "group"];
  environment = environment;
}
