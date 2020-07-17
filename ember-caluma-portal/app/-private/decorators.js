import { decoratorWithRequiredParams } from "@ember-decorators/utils/decorator";
import { getOwner } from "@ember/application";
import { assert } from "@ember/debug";
// eslint-disable-next-line ember/no-observers
import { computed, observer } from "@ember/object";
import { reads } from "@ember/object/computed";
import { classify } from "@ember/string";
import normalizeAbilityString from "ember-can/utils/normalize";

/**
 * A decorator to require a certain ember-can permission for a route. If the
 * permission is denied the route renders a different template (by default
 * "notfound"). This also implements a loading state if the permission model is
 * still loading.
 *
 * Example usage:
 * ```js
 * // foo/route.js
 * import Route from "@ember/route";
 * import { can } from "ember-caluma-portal/-private/decorators"
 *
 * @can("list users")
 * class TestRoute extends Route {
 *   model() {
 *     return fetch("/api/v1/users")
 *   };
 * }
 *
 * export default TestRoute
 * ```
 *
 * Advanced usage with `ember-concurrency` tasks on the controller as model and
 * `ember-can`s additional attributes:
 *
 * ```js
 * // abilities/user.js
 * import Ability from "ember-can";
 * import { computed } from "@ember/object";
 *
 * export class UserAbility extends Ability {
 *   @computed("model", "userType")
 *   get canList() {
 *     return this.model && !this.userType === "admin";
 *   };
 * };
 * ```
 *
 * ```js
 * // foo/controller.js
 * import Controller from "@ember/controller";
 * import { restartableTask } from "ember-concurrency-decorators";
 *
 * export default class TestController extends Controller {
 *   userType = "admin";
 *
 *   @lastValue("dataTask") data
 *   @restartableTask
 *   *dataTask() {
 *     return yield fetch("/api/v1/users")
 *   };
 * };
 * ```
 *
 * ```js
 * // foo/route.js
 * import Route from "@ember/route";
 * import { can } from "ember-caluma-portal/-private/decorators"
 *
 * @can("list users", {
 *   model: "controller.data",
 *   loading: "controller.dataTask.isRunning",
 *   additionalAttributes: { userType: "controller.userType" }
 * })
 * class TestRoute extends Route {};
 *
 * export default TestRoute;
 * ```
 *
 * @function can
 * @param {String} permission The permission string consumed by the ember-can ability
 * @param {Object} options The options for the route
 * @param {String} options.model The property name of the permission model
 * @param {String} options.template The name of the template to render when permission is denied
 * @param {String} options.loading The property name of the permission models loading state
 * @param {String} options.loadingTemplate The name of the template to render when the permission model is loading
 * @param {Object} options.additionalAttributes The additional attributes for the ability, the key is the property name in the ability and the value is the property name of the value
 * @returns {Function} The decorator function
 * @public
 */
export const can = decoratorWithRequiredParams(
  (
    target,
    [
      permission,
      {
        model = "controller.model",
        template = "notfound",
        loading = "controller.model.isPending",
        loadingTemplate = "loading",
        additionalAttributes = {},
      } = {},
    ]
  ) => {
    const { propertyName, abilityName } = normalizeAbilityString(permission);

    target.reopen({
      _ability: computed(function () {
        const Factory = getOwner(this).factoryFor(`ability:${abilityName}`);

        assert(`No ability type found for '${abilityName}'`, Factory);

        const aliases = {
          // create an alias for the abilitys model to the data in the route
          model: reads(`_target.${model}`),
          // create an alias for each of the additional attributes to the data in the route

          ...Object.entries(additionalAttributes).reduce((obj, [key, path]) => {
            return { ...obj, [key]: reads(`_target.${path}`) };
          }, {}),
        };

        // we need to inject the route into the ability so we can use the routes data
        return Factory.create({ _target: this }).reopen(aliases);
      }),

      _can: reads(`_ability.can${classify(propertyName)}`),

      // eslint-disable-next-line ember/no-observers
      _rerenderTemplate: observer("templateName", function () {
        this.renderTemplate();
      }),

      templateName: computed("_can", loading, function () {
        return this.get(loading)
          ? loadingTemplate // permission model is still loading - render custom template (loading)
          : !this._can
          ? template // permission is denied - render custom template (notfound)
          : target.templateName; // user has permission - render the default template
      }),
    });

    return target;
  }
);

export default { can };
