import Helper from "@ember/component/helper";
import { service } from "@ember/service";
import { cell, resource, use, resourceFactory } from "ember-resources";
import { dedupeTracked } from "tracked-toolbox";

export const HasPermission = resourceFactory((argsFn) => {
  return resource(({ owner }) => {
    const value = cell(false);

    const [requireAll, instanceId, requiredPermissions, reload] = argsFn();
    const fn = requireAll ? "hasAll" : "hasAny";

    owner
      .lookup("service:permissions")
      [fn](instanceId, requiredPermissions, reload)
      .then((resolved) => value.set(resolved))
      .catch(() => value.set(false));

    return value;
  });
});

export default class HasPermissionHelper extends Helper {
  @service permissions;

  @dedupeTracked instanceId = undefined;
  @dedupeTracked requiredPermissions = undefined;
  @dedupeTracked reload = undefined;

  requireAll = false;

  condition = use(
    this,
    HasPermission(() => [
      this.requireAll,
      this.instanceId,
      this.requiredPermissions?.split(",") ?? [],
      this.reload,
    ]),
  );

  compute(
    [instanceId, ...requiredPermissions],
    { reload = false, invert = false } = {},
  ) {
    this.reload = reload;
    this.instanceId = instanceId;
    this.requiredPermissions = requiredPermissions.flat().join(","); // needed in order for dedupeTracked to work

    const result = this.condition.current;

    return invert ? !result : result;
  }
}
