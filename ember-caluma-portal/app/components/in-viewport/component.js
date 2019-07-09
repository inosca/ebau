import Component from "@ember/component";

export default Component.extend({
  didInsertElement() {
    this._super(...arguments);

    const observer = new IntersectionObserver(entries => {
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

  willDestroyObject() {
    this._super(...arguments);

    this.observer.disconnect();
  }
});
