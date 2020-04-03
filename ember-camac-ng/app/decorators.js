import { getOwner } from "@ember/application";

export function loadingTask(target, property, desc) {
  const gen = desc.value;

  desc.value = function*(...args) {
    try {
      getOwner(this)
        .lookup("controller:application")
        .set("loading", true);

      return yield* gen.apply(this, args);
    } finally {
      getOwner(this)
        .lookup("controller:application")
        .set("loading", false);
    }
  };

  return desc;
}

export default { loadingTask };
