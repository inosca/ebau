import { getOwnConfig } from "@embroider/macros";
import { test as qunitTest } from "qunit";

const app = getOwnConfig()?.application;

// Lifted from qunit
function extend(a, b, undefOnly) {
  for (const prop in b) {
    if (Object.prototype.hasOwnProperty.call(b, prop)) {
      if (b[prop] === undefined) {
        delete a[prop];
      } else if (!(undefOnly && typeof a[prop] !== "undefined")) {
        a[prop] = b[prop];
      }
    }
  }
  return a;
}

function runIfApp(fn, target) {
  return function (name, ...args) {
    if (app === target) {
      return fn(`${name} [${target.toUpperCase()}]`, ...args);
    }
  };
}

export function testForApp(target) {
  return extend(runIfApp(qunitTest, target), {
    todo: runIfApp(qunitTest.todo, target),
    skip: runIfApp(qunitTest.skip, target),
    only: runIfApp(qunitTest.only, target),
    each: runIfApp(qunitTest.each, target),
  });
}

export const testBE = testForApp("be");
export const testSZ = testForApp("sz");
export const testUR = testForApp("ur");
export const testGR = testForApp("gr");
export const test = testForApp("test");
