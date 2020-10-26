import { getOwner } from "@ember/application";
import { tracked } from "@glimmer/tracking";

export function loadingTask(target, property, desc) {
  const gen = desc.value;

  desc.value = function* (...args) {
    try {
      getOwner(this).lookup("controller:application").set("loading", true);

      return yield* gen.apply(this, args);
    } finally {
      getOwner(this).lookup("controller:application").set("loading", false);
    }
  };

  return desc;
}

export function objectFromQueryParams(...fields) {
  // There is no easy way of putting the fileds directly into the queryParams array.
  // So you need to set the array yourself.
  return function (target, property, desc) {
    fields.forEach((field) => {
      Object.defineProperty(
        target,
        field,
        tracked(target, field, {
          value: target[field],
          enumerable: true,
          configurable: true,
          writable: true,
          initializer: null,
        })
      );
    });

    delete desc.writable;
    delete desc.configurable;
    delete desc.initializer;
    delete desc.enumerable;

    desc.get = function () {
      return Object.assign(
        ...fields.map((field) => ({
          [field]: this[field],
        }))
      );
    };
    desc.set = function (object) {
      fields.forEach((key) => {
        this[key] = object[key];
      });
    };

    return desc;
  };
}

export default { loadingTask, objectFromQueryParams };
