const applyTestQueryParamsFilter = (models, queryParams) => {
  // This is a very naive implementation for picking all "filter[SOMEPROPERTY]" query params
  // and will only work for single level nesting.
  const filter = {};
  Object.entries(queryParams)
    .filter(([k]) => k.startsWith("filter"))
    .forEach(([k, v]) => {
      if (v) {
        const key = k.replace("filter[", "").replace("]", "");
        filter[key] = v;
      }
    });
  if (!Object.keys(filter).length) {
    return models;
  }

  // The sole purpose of this "deep filtering" is to support the nested "access-level.slug" filter
  // on instance-acls.
  // TODO: remove this when access-level filtering is specificed and implemented
  const valueForKey = (obj, qsStringOrKeys) => {
    const keys = Array.isArray(qsStringOrKeys)
      ? qsStringOrKeys
      : qsStringOrKeys.split(".");
    if (keys.length > 1) {
      return valueForKey(obj[keys.shift()], keys);
    }
    return obj[keys[0]];
  };
  return models.filter((model) =>
    Object.keys(filter).every((key) => valueForKey(model, key) === filter[key]),
  );
};

export default applyTestQueryParamsFilter;
