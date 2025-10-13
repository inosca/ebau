import NotificationService from "ember-uikit/services/notification";

export default class CustomNotificationService extends NotificationService {
  danger(msg, ...args) {
    return super.danger(this.prependIcon(msg, "danger"), ...args);
  }

  success(msg, ...args) {
    return super.success(this.prependIcon(msg, "success"), ...args);
  }

  warning(msg, ...args) {
    return super.warning(this.prependIcon(msg, "warning"), ...args);
  }

  primary(msg, ...args) {
    return super.primary(this.prependIcon(msg, "primary"), ...args);
  }

  prependIcon(msg, type) {
    const iconMap = {
      danger: "ban",
      primary: "info",
      success: "check",
      warning: "warning",
    };

    return `<span uk-icon="${iconMap[type]}"></span>${msg}`;
  }
}
