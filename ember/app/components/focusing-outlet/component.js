/* eslint-disable ember/no-observers */
import { getOwner } from "@ember/application";
import { action, get } from "@ember/object";
import { scheduleOnce } from "@ember/runloop";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

/*
 * This component has been copied form ember-a11y to be ember-octane compatible
 * https://github.com/ember-a11y/ember-a11y/blob/v0.2.2/addon/components/focusing-inner.js
 */
export default class FocusingOutletComponent extends Component {
  @tracked shouldFocus = false;
  @tracked element;
  outletName = "main";

  @action
  processChange(element) {
    this.element = element;
    const application = getOwner(this).lookup("application:main");
    const pivotHandler = application.get(
      "_stashedHandlerInfos.pivotHandler.name"
    );

    // Supports Handlebars version which stores information up one level.
    const outletObject = this.args.outletState.outlets || this.args.outletState;

    const currentRoute = get(outletObject, `${this.outletName}.render.name`);
    if (!currentRoute) {
      return;
    }

    const isFirstVisit = pivotHandler === undefined;
    const isPivot = pivotHandler === currentRoute;
    const isChildState = ~["loading", "error"].indexOf(
      currentRoute.split(".").pop()
    );
    const isSubstate =
      ~currentRoute.indexOf("_loading") || ~currentRoute.indexOf("_error");

    const shouldFocus =
      !isFirstVisit && (isPivot || isChildState || isSubstate);
    this.shouldFocus = shouldFocus;

    this.scheduleFocus();
  }

  scheduleFocus() {
    const owner = getOwner(this);
    const environment = owner.lookup("-environment:main");

    // Assume that we're interactive by default to support old Ember.
    let isInteractive = true;

    // However, if we're in a version of Ember that explicitly sets
    // `isInteractive` we will instead defer to that.
    if (
      environment &&
      Object.prototype.hasOwnProperty.call(environment, "isInteractive")
    ) {
      isInteractive = environment.isInteractive;
    }

    if (!isInteractive || !this.element) {
      return;
    }

    if (this.shouldFocus && !this.isDestroyed && !this.isDestroying) {
      // We need to wait until the content is rendered into the outlet before setting focus.
      scheduleOnce("afterRender", this, "setFocus");
    } else {
      this.element.removeAttribute("tabindex");
      this.element.removeAttribute("role");
    }
  }

  setFocus() {
    if (!this.element) {
      return;
    }

    if (this.shouldFocus && !this.isDestroyed && !this.isDestroying) {
      // Just in case it is currently focused.
      this.element.blur();

      // We have to make the element interactive prior to focusing it.
      this.element.setAttribute("tabindex", "-1");
      this.element.setAttribute("role", "group");
      this.scrollPositionFocus();
    }
  }

  scrollPositionFocus() {
    const parents = [];

    for (let current = this.element; current; current = current.parentNode) {
      parents.push({
        element: current,
        scrollTop: current.scrollTop,
        scrollLeft: current.scrollLeft,
      });
    }

    // this.element.focus();

    // Reset the scroll position for the entire hierarchy.
    for (let i = 0; i < parents.length; i++) {
      const scrollConfig = parents[i];
      const element = scrollConfig.element;

      element.scrollTop = scrollConfig.scrollTop;
      element.scrollLeft = scrollConfig.scrollLeft;
    }
  }
}
