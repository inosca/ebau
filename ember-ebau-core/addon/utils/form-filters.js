export const groupFormsByCategories = (
  forms,
  categories,
  intl,
  translationString = (group) => `cases.formCategories.${group}`,
) => {
  return categories
    .map((category) => {
      const options = forms
        .filter((form) => form.category === category)
        .sort((a, b) => a.order - b.order);

      return options.length
        ? {
            groupName: intl.t(translationString(category)),
            options,
          }
        : null;
    })
    .filter(Boolean);
};

export const getRecursiveSources = (form, forms) => {
  if (!form.source?.slug) {
    return [];
  }

  const source = forms.find((edge) => edge.node.slug === form.source.slug);

  return [source.node.slug, ...getRecursiveSources(source.node, forms)];
};

export default { getRecursiveSources, groupFormsByCategories };
