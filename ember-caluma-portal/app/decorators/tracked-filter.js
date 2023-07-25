import { tracked } from "@glimmer/tracking";
import { TrackedObject } from "tracked-built-ins";
import { cached } from "tracked-toolbox";

/**
 * Decorator to define an intermediate filter that stores the filters in a
 * tracked object and only applies them to the real property when the apply
 * function is called.
 *
 * This decorator takes a serialize and deserialize function which are used to
 * process the input value.
 *
 * It provides an `_applyFilters` and `_resetFilters` method on the current
 * object as well as a `_filters` tracked object which stores the intermediate
 * filters including their dirty state and a `_filtersConfig` object which holds
 * the filter configuration.
 *
 * Usage example:
 *
 * ```js
 * export default class MyController extends Controller {
 *   get queryParams() {
 *     return this._filtersConfig.map(({ privateKey, publicKey }) => ({
 *       [privateKey]: publicKey,
 *     }));
 *   }
 *
 *   @trackedFilter({ defaultValue: 1 }) id;
 *   @trackedFilter({
 *     serialize(value) {
 *       return value.join(",");
 *     },
 *     deserialize(value) {
 *       return value.split(",");
 *     },
 *   })
 *   types;
 *
 *   @action apply() {
 *     this._applyFilters()
 *   }
 *
 *   @action reset() {
 *     this._resetFilters()
 *   }
 * }
 * ```
 */
export default function trackedFilter({
  serialize = (value) => value,
  deserialize = (value) => value,
  defaultValue,
}) {
  return function decorator(target, property) {
    if (!Object.prototype.hasOwnProperty.call(target, "_filters")) {
      target._filters = new TrackedObject();
      target._applyFilters = function () {
        this._filtersConfig.forEach(
          ({ privateKey, publicKey, dirtyKey, serialize }) => {
            this[privateKey] = serialize.call(this, this[publicKey]);
            this._filters[dirtyKey] = false;
          },
        );
      };
      target._resetFilters = function () {
        this._filtersConfig.forEach(
          ({ publicKey, privateKey, dirtyKey, defaultValue }) => {
            this._filters[publicKey] = defaultValue;
            this._filters[dirtyKey] = false;
            this[privateKey] = defaultValue;
          },
        );
      };
    }

    const privateKey = `_${property}`;
    const dirtyKey = `${property}Dirty`;

    Object.defineProperty(
      target,
      privateKey,
      tracked(target, privateKey, { initializer: () => defaultValue }),
    );

    target._filters[property] = defaultValue;
    target._filters[dirtyKey] = false;
    target._filtersConfig = [
      ...(target._filtersConfig ?? []),
      {
        privateKey,
        publicKey: property,
        dirtyKey,
        serialize,
        deserialize,
        defaultValue,
      },
    ];

    return cached(target, property, {
      enumerable: true,
      configurable: false,
      get() {
        const filtersValue = this._filters[property];
        const targetValue = this[privateKey];

        const value =
          filtersValue === defaultValue &&
          targetValue !== defaultValue &&
          !this._filters[dirtyKey]
            ? targetValue
            : filtersValue;

        return deserialize.call(this, value);
      },
      set(value) {
        this._filters[property] = serialize.call(this, value);
        this._filters[dirtyKey] = true;
      },
    });
  };
}
