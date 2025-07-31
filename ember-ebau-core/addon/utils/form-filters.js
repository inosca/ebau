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

export const removeVersion = (formSlug) => formSlug?.replace(/-v\d+$/, "");

/**
 * Get versioned sources of a given form.
 *
 * This is used in form filters of case lists. In order to make sure to get all
 * dossiers with any version of a form, we need to filter for previous versions
 * of a form as well. To do this, we assume that versioned forms have the
 * previous form version as `source` property and the slug is the same but with
 * a version suffix (e.g. ...-v2).
 */
export const getRecursiveSources = (form, forms) => {
  const sourceSlug = form.source?.slug;

  if (!sourceSlug || removeVersion(sourceSlug) !== removeVersion(form.slug)) {
    return [];
  }

  const source = forms.find((edge) => edge.node.slug === sourceSlug);

  return [sourceSlug, ...getRecursiveSources(source.node, forms)];
};

export default { getRecursiveSources, groupFormsByCategories };
