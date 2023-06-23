import { getOwnConfig } from "@embroider/macros";
import { test } from "qunit";

const app = getOwnConfig()?.application;

export function testForApp(target) {
  return function (name, ...args) {
    if (app === target) {
      return test(`${name} [${target.toUpperCase()}]`, ...args);
    }
  };
}

export const testBE = testForApp("be");
export const testSZ = testForApp("sz");
export const testUR = testForApp("ur");
export const testGR = testForApp("gr");
