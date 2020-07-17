import Component from "@ember/component";

export default Component.extend({
  didInsertElement(...args) {
    this._super(...args);

    const observer = new IntersectionObserver((entries) => {
      const action = this.getWithDefault("onEnter");

      if (action && typeof action === "function") {
        entries.forEach(({ isIntersecting }) => {
          if (isIntersecting) {
            action.apply(this);
          }
        });
      }
    }, {});

    // this is not an ember observer but an introspection observer
    // eslint-disable-next-line ember/no-observers
    observer.observe(this.element);

    this.set("observer", observer);
  },

  willDestroyObject(...args) {
    this._super(...args);

    this.observer.disconnect();
  },
});
