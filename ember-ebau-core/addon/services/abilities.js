import AbilitiesService from "ember-can/services/abilities";

// https://github.com/minutebase/ember-can/pull/182
export default class AsyncAbilitiesService extends AbilitiesService {
  #getResult(abilityString, model, properties, invert = false) {
    const { propertyName, abilityName } = this.parse(abilityString);
    const result = this.valueFor(propertyName, abilityName, model, properties);

    /* `Promise` might be an RSVP Promise here, so to match native JS promises
     * (returned from async methods), we need some duck-typing.
     * TODO: Remove the second clause again as soon as all remnants of RSVP are
     * gone from the source code.
     */
    if (result instanceof Promise || typeof result?.then === "function") {
      return result
        .then((bool) => (invert ? !bool : !!bool))
        .catch((error) => {
          console.error(error);
          return invert;
        });
    }

    return invert ? !result : !!result;
  }

  can(abilityString, model, properties) {
    return this.#getResult(abilityString, model, properties, false);
  }

  cannot(abilityString, model, properties) {
    return this.#getResult(abilityString, model, properties, true);
  }
}
