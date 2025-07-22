export function moduleConfig(moduleName, configKey, defaultValue) {
  return function () {
    return {
      get() {
        return (
          this.shoebox.content.config?.[moduleName]?.[configKey] ?? defaultValue
        );
      },
    };
  };
}

export default { moduleConfig };
