import { test, skip } from "qunit";

import config from "ember-caluma-portal/config/environment";

export default function testIf(appName) {
  if (config.APPLICATION.name === appName) {
    return test;
  }
  return skip;
}
