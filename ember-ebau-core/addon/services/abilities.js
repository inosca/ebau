import AbilitiesService from "ember-can/services/abilities";

// https://github.com/minutebase/ember-can/pull/182
export default class AsyncAbilitiesService extends AbilitiesService {
  #getResult(abilityString, model, properties, invert = false) {
    const { propertyName, abilityName } = this.parse(abilityString);
    const result = this.valueFor(propertyName, abilityName, model, properties);

    if (result instanceof Promise) {
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
