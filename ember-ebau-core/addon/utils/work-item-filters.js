export function cleanTaskAndTemplateFilters(filters) {
  return (
    filters
      // Remove all task filters
      .filter((flt) => !flt.task)
      .map((flt) => {
        if (flt.metaValue) {
          // Remove meta value filters that filter for the key "template-id"
          return {
            ...flt,
            metaValue: flt.metaValue.filter(
              (metaFlt) => metaFlt.key !== "template-id",
            ),
          };
        }

        return flt;
      })
  );
}

function addTaskFilter(filters, slug) {
  return [...filters, { task: slug }];
}

function addTemplateFilter(filters, uuid) {
  const templateFilter = { key: "template-id", value: uuid };
  const existingMetaFilter = filters.find((flt) => flt.metaValue);

  if (existingMetaFilter) {
    // If there's already a meta value filter, we extend it with the new filter
    // for the template
    return [
      ...filters.filter((flt) => !flt.metaValue),
      {
        metaValue: [...existingMetaFilter.metaValue, templateFilter],
      },
    ];
  }

  // If not, we add it
  return [...filters, { metaValue: [templateFilter] }];
}

export function addTaskOrTemplateFilter(originalFilters, type, slugOrUuid) {
  const cleanedFilters = cleanTaskAndTemplateFilters(originalFilters);

  if (type === "task") {
    return addTaskFilter(cleanedFilters, slugOrUuid);
  } else if (type === "template") {
    return addTemplateFilter(cleanedFilters, slugOrUuid);
  }

  return cleanedFilters;
}

export default {
  cleanTaskAndTemplateFilters,
  addTaskOrTemplateFilter,
};
