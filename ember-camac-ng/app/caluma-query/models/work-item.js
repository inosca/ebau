import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import WorkItemModel from "ember-caluma/caluma-query/models/work-item";

import saveWorkItemMutation from "camac-ng/gql/mutations/save-workitem";

export default class CustomWorkItemModel extends WorkItemModel {
  @service store;
  @service shoebox;
  @service router;
  @service apollo;
  @service intl;
  @service notifications;

  @tracked notViewed = this.raw.meta["not-viewed"];
  @tracked assignedUsers = this.raw.assignedUsers;
  @tracked addressedGroups = this.raw.addressedGroups;

  get assignedUser() {
    return this.store
      .peekAll("user")
      .find(user => this.assignedUsers.includes(user.username));
  }

  get addressedService() {
    return this.store
      .peekAll("service")
      .find(service => this.addressedGroups.includes(service.id));
  }

  get isAddressed() {
    return (
      parseInt(this.addressedService?.id) === this.shoebox.content.serviceId
    );
  }

  get responsible() {
    if (this.isAddressed) {
      return this.assignedUser?.fullName || "-";
    }

    return [
      this.addressedService.name,
      this.assignedUser ? `(${this.assignedUser.fullName})` : ""
    ].join(" ");
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get case() {
    return this.raw.case.parentWorkItem?.case || this.raw.case;
  }

  get instanceId() {
    return this.case?.meta["camac-instance-id"];
  }

  get instanceName() {
    const identifier = this.instance?.identifier || this.instanceId;
    const name = this.instance?.name || this.case?.document.form.name;
    const ebauNr = this.case?.meta["ebau-number"];
    const suffix = ebauNr ? `(${ebauNr})` : "";

    return `${identifier} - ${name} ${suffix}`.trim();
  }

  get closedByUser() {
    return this.store.peekAll("user").findBy("username", this.raw.closedByUser);
  }

  get createdByUser() {
    return this.store
      .peekAll("user")
      .findBy("username", this.raw.createdByUser);
  }

  get isAssignedToCurrentUser() {
    return this.assignedUsers.includes(this.shoebox.content.username);
  }

  get canEdit() {
    return this.isAddressed && this.raw.status === "READY";
  }

  get directLink() {
    const link = this._getDirectLinkFor(this.raw.task.slug);

    return (
      (this.canEdit && link) ||
      `/index/redirect-to-instance-resource/instance-id/${this.instanceId}`
    );
  }

  get editLink() {
    const url = this._getDirectLinkFor("edit");
    const hash = this.router.urlFor(
      "work-items.instance.edit",
      this.instanceId,
      this.id
    );

    return this.canEdit && url && `${url}${hash}`;
  }

  _getDirectLinkFor(configKey) {
    try {
      const config = this.shoebox.content.config.directLink;
      const role = this.shoebox.role;

      const template = config[configKey][role];
      const data = {
        INSTANCE_ID: this.instanceId,
        CIRCULATION_ID: this.raw.meta["circulation-id"],
        ACTIVATION_ID: this.raw.meta["activation-id"]
      };

      return Object.entries(data).reduce(
        (str, [key, value]) => str.replace(`{{${key}}}`, value),
        template
      );
    } catch (error) {
      return null;
    }
  }

  async markAsRead() {
    try {
      this.notViewed = false;

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            meta: JSON.stringify({ ...this.raw.meta, "not-viewed": false })
          }
        }
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.saveError"));
    }
  }

  async assignToMe() {
    await this.assignToUser({ username: this.shoebox.content.username });
  }

  async assignToUser(user) {
    try {
      this.assignedUsers = [user.username];

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            assignedUsers: this.assignedUsers
          }
        }
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.saveError"));
    }
  }

  static fragment = `{
    createdAt
    createdByUser
    createdByGroup
    closedAt
    closedByUser
    closedByGroup
    status
    meta
    addressedGroups
    controllingGroups
    assignedUsers
    name
    deadline
    description
    case {
      id
      meta
      document {
        form {
          name
        }
      }
      parentWorkItem {
        case {
          meta
          document {
            form {
              name
            }
          }
        }
      }
    }
    task {
      slug
    }
  }`;
}
