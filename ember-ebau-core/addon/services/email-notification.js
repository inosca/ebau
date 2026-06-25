import Service, { service } from "@ember/service";

export default class EmailNotificationService extends Service {
  @service fetch;

  /**
   * Send an email notification for a specific instance.
   *
   * @param {Number} instanceId The ID of the instance related to the notification
   * @param {String} templateSlug The template slug to send
   * @param {Array<String>} recipientTypes An array of recipient types
   * @param {Object} extraRelationships Extra relationships if necessary (e.g. inquiry)
   */
  async send(
    instanceId,
    templateSlug,
    recipientTypes,
    extraRelationships = {},
  ) {
    await this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
      method: "POST",
      headers: {
        accept: "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
      },
      body: JSON.stringify({
        data: {
          type: "notification-template-sendmails",
          attributes: {
            "template-slug": templateSlug,
            "recipient-types": recipientTypes,
          },
          relationships: {
            instance: { data: { type: "instances", id: instanceId } },
            ...extraRelationships,
          },
        },
      }),
    });
  }
}
