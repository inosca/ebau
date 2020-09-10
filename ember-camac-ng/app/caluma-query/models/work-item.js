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

  get assignedUserInformation() {
    return this.store
      .peekAll("user")
      .filter(user => this.assignedUsers.includes(user.username));
  }

  get addressedServices() {
    return this.store
      .peekAll("service")
      .filter(service => this.addressedGroups.includes(service.id));
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get instanceIdentifier() {
    const szIdentifier = this.instance?.identifier;

    const ebauNr = this.case?.meta["ebau-number"];
    const beIdentifier = ebauNr
      ? `${this.instanceId} (${ebauNr})`
      : this.instanceId;

    return szIdentifier || beIdentifier;
  }

  get case() {
    return this.raw.case.parentWorkItem?.case || this.raw.case;
  }

  get instanceId() {
    return this.case?.meta["camac-instance-id"];
  }

  get instanceName() {
    return this.instance?.name || this.case.document.form.name;
  }

  get instanceLink() {
    return `/index/redirect-to-instance-resource/instance-id/${this.instanceId}`;
  }

  get closedByUser() {
    return this.store.peekAll("user").findBy("username", this.raw.closedByUser);
  }

  get createdByUser() {
    return this.store
      .peekAll("user")
      .findBy("username", this.raw.createdByUser);
  }

  get isAddressedToCurrentService() {
    return this.addressedGroups
      .map(id => parseInt(id))
      .includes(this.shoebox.content.serviceId);
  }

  get isAssignedToCurrentUser() {
    return this.assignedUsers.includes(this.shoebox.content.username);
  }

  get canEdit() {
    return this.isAddressedToCurrentService && this.raw.status === "READY";
  }

  get directLink() {
    if (!this.canEdit) return null;

    const config = this.shoebox.content.config.directLink;
    const role = this.shoebox.role;
    const task = this.raw.task.slug;

    try {
      const template = config[task][role];
      const data = {
        INSTANCE_ID: this.instanceId,
        CIRCULATION_ID: this.raw.meta["circulation-id"],
        ACTIVATION_ID: this.raw.meta["activation-id"]
      };

      return Object.entries(data).reduce(
        (str, [key, value]) => str.replace(new RegExp(`{{${key}}}`), value),
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
