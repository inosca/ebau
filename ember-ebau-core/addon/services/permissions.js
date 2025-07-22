import Service, { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class PermissionsService extends Service {
  @service store;
  @service fetch;

  #cache = new Map();

  @tracked fullyEnabled = false;
  @tracked mode = null;

  async setup() {
    const response = await this.fetch.fetch("/api/v1/permissions-meta");
    const { data } = await response.json();

    this.fullyEnabled = data["fully-enabled"];
    this.mode = data["permission-mode"];
  }

  async #triggerCache(instanceId, reload) {
    if (!instanceId) return;

    let grantedPermissions = [];

    try {
      let model = this.store.peekRecord("instance-permission", instanceId);

      if (!model || reload) {
        model = await this.store.findRecord("instance-permission", instanceId, {
          reload: true,
        });
      }

      grantedPermissions = model.permissions;
    } catch {
      // That's ok, if no permissions could be fetched we assume that we don't
      // have any.
    }

    this.#cache.set(parseInt(instanceId), grantedPermissions);
  }

  #checkPermissions(instanceId, requiredPermissions, requireAll) {
    if (!instanceId || !requiredPermissions?.length) {
      return false;
    }

    requiredPermissions = Array.isArray(requiredPermissions)
      ? requiredPermissions.flat()
      : [requiredPermissions];

    const grantedPermissions = this.#cache.get(parseInt(instanceId)) ?? [];
    const has = (permission) => grantedPermissions.includes(permission);

    return requireAll
      ? requiredPermissions.every(has)
      : requiredPermissions.some(has);
  }

  /**
   * Check if user has at least one of the required permissions.
   *
   * @param {Number} instanceId - The ID of the instance to check the permissions for
   * @param {Array<String>} requiredPermissions - An array of required permissions
   * @param {Boolean} reload - Force a request to the API
   * @returns {Promise<Boolean>}
   */
  async hasAny(instanceId, requiredPermissions, reload = false) {
    await this.#triggerCache(instanceId, reload);
    return this.#checkPermissions(instanceId, requiredPermissions, false);
  }

  /**
   * Check if user has all of the required permissions.
   *
   * @param {Number} instanceId - The ID of the instance to check the permissions for
   * @param {Array<String>} requiredPermissions - An array of required permissions
   * @param {Boolean} reload - Force a request to the API
   * @returns {Promise<Boolean>}
   */
  async hasAll(instanceId, requiredPermissions, reload = false) {
    await this.#triggerCache(instanceId, reload);
    return this.#checkPermissions(instanceId, requiredPermissions, true);
  }

  /**
   * Populate the permissions cache for a given instance.
   *
   * This method is helpful for fetching the permissions of an instance before
   * rendering anything so the permissions helpers resolve instantly afterwards.
   * This prevents the UI from flickering.
   *
   * @param {Number} instanceId - The ID of the instance to populate the cache for
   * @returns {Promise}
   */
  async populateCacheFor(instanceId) {
    await this.#triggerCache(instanceId, true);
  }
}
