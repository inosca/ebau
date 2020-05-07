import Router from "@ember/routing/router";

const stashedHandlerInfos = {};

Router.reopen({
  init(...args) {
    this.on("routeWillChange", transition => {
      const oldRoute = transition.from;
      const newRoute = transition.to;

      if (oldRoute === null || newRoute === null) {
        return undefined;
      }
      if (oldRoute.localName !== newRoute.localName) {
        return newRoute;
      }

      stashedHandlerInfos.pivotHandler = newRoute;
    });
    this._super(...args);
  }
});

export function initialize(instance) {
  const lookupContext = instance.lookup ? instance : instance.container;
  lookupContext.lookup(
    "application:main"
  )._stashedHandlerInfos = stashedHandlerInfos;
}

export default {
  initialize
};
