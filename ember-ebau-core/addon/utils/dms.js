export const MIME_TYPE_TO_ENGINE = {
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
    "xlsx-template",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    "docx-template",
};

export const MIME_TYPE_TO_EXTENSION = {
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    ".docx",
};

export function sortByDescription(a, b) {
  return a?.description?.localeCompare(b?.description);
}

/**
 * Recursively filter complex placeholder data (one item of an array value)
 * based on the available aliases in the given language.
 *
 * const item = {
 *   date: 1,
 *   datum: 1,
 *   opposing: [
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *   ],
 *   einsprechende: [
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *   ],
 *   user: {
 *     firstName: "some",
 *     lastName: "name"
 *   },
 *   benutzer: {
 *     vorname: "some",
 *     nachname: "name"
 *   },
 * };
 *
 * const aliases = {
 *   date: [{ de: "datum" }],
 *   opposing: [{ de: "einsprechende" }],
 *   "opposing.address": [{ de: "adresse" }],
 *   user: [{de: "benutzer"}],
 *   "user.firstName": [{de: "vorname"}],
 *   "user.lastName": [{de: "nachname"}],
 * };
 *
 * const result = parseNested(item, aliases, "de")
 *
 * Will return the following structure:
 *
 * const result =  {
 *   datum: 1,
 *   einsprechende: [
 *     {
 *       adresse: 1,
 *     },
 *     {
 *       adresse: 1,
 *     },
 *   ],
 *   benutzer: {
 *      vorname: "some",
 *      nachname: "name",
 *   }
 * };
 */
export function parseNested(data, aliases, locale) {
  if (!data) return data;

  if (Array.isArray(data)) {
    return data.map((item) => transformItem(item, aliases, locale));
  }

  return transformItem(data, aliases, locale);
}

function transformItem(item, aliases, locale) {
  if (!item || typeof item !== "object") return item;

  return Object.entries(item).reduce((prev, [key, value]) => {
    const alias = aliases[key]?.[0]?.[locale];

    if (!alias) {
      return prev;
    }

    const doubleNestedRe = new RegExp(`^${key}\\.`);

    const doubleNested = Object.entries(aliases).reduce(
      (_prev, [nestedKey, nestedAliases]) => {
        if (nestedKey.search(doubleNestedRe) < 0) {
          return _prev;
        }

        return {
          ..._prev,
          [nestedKey.replace(doubleNestedRe, "")]: nestedAliases,
        };
      },
      {},
    );

    if (value && Object.keys(doubleNested).length) {
      value = parseNested(value, doubleNested, locale);
    }

    return { ...prev, [alias]: value };
  }, {});
}
