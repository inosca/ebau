import { setupMirage } from "ember-cli-mirage/test-support";
import { Response } from "miragejs";

class PermissionManager {
  #permissions = new Map();

  grant(instanceId, permissions) {
    if (!this.#permissions.has(instanceId)) {
      this.#permissions.set(instanceId, new Set());
    }

    const cache = this.#permissions.get(instanceId);

    permissions.forEach((permission) => {
      cache.add(permission);
    });
  }

  revoke(instanceId, permissions) {
    if (!this.#permissions.has(instanceId)) {
      return;
    }

    const cache = this.#permissions.get(instanceId);

    permissions.forEach((permission) => {
      cache.delete(permission);
    });
  }

  getResponse(instanceId) {
    return new Response(
      200,
      {},
      {
        data: {
          id: String(instanceId),
          type: "instance-permissions",
          attributes: {
            permissions: [...(this.#permissions.get(instanceId) ?? [])],
          },
          relationships: {
            instance: {
              data: {
                id: String(instanceId),
                type: "instances",
              },
            },
          },
        },
      },
    );
  }

  getAll(instanceId) {
    return this.#permissions.get(instanceId);
  }
}

export default function setupPermissions(
  hooks,
  instanceId = null,
  initialPermissions = [],
) {
  setupMirage(hooks);

  hooks.beforeEach(function () {
    const manager = new PermissionManager();

    this.permissions = manager;

    if (instanceId) {
      this.permissions.grant(instanceId, initialPermissions);
    }

    this.server.get("/api/v1/instance-permissions/:id", function (_, request) {
      return manager.getResponse(parseInt(this._getIdForRequest(request)));
    });
  });
}
