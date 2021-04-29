import { test, skip } from "qunit";

import config from "caluma-portal/config/environment";

export default function testIf(appName) {
  if (config.APPLICATION.name === appName) {
    return test;
  }
  return skip;
}
