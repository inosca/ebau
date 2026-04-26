import { setupMirage } from "ember-cli-mirage/test-support";
import { Response } from "miragejs";

class PermissionManager {
  #permissions = new Map();

  constructor(owner) {
    this.service = owner.lookup("service:permissions");
  }

  grant(instanceId, permissions) {
    instanceId = parseInt(instanceId);

    if (!this.#permissions.has(instanceId)) {
      this.#permissions.set(instanceId, new Set());
    }

    const cache = this.#permissions.get(instanceId);

    permissions.forEach((permission) => {
      cache.add(permission);
    });

    this.service.clearCacheFor(instanceId);
  }

  revoke(instanceId, permissions) {
    instanceId = parseInt(instanceId);

    if (!this.#permissions.has(instanceId)) {
      return;
    }

    const cache = this.#permissions.get(instanceId);

    permissions.forEach((permission) => {
      cache.delete(permission);
    });

    this.service.clearCacheFor(instanceId);
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
            permissions: [
              ...(this.#permissions.get(parseInt(instanceId)) ?? []),
            ],
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
    return this.#permissions.get(parseInt(instanceId));
  }
}

export default function setupPermissions(
  hooks,
  instanceId = null,
  initialPermissions = [],
) {
  setupMirage(hooks);

  hooks.beforeEach(function () {
    const manager = new PermissionManager(this.owner);

    this.permissions = manager;

    if (instanceId) {
      this.permissions.grant(instanceId, initialPermissions);
    }

    this.server.get("/api/v1/instance-permissions/:id", function (_, request) {
      return manager.getResponse(parseInt(this._getIdForRequest(request)));
    });
  });
}
