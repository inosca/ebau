export async function fetchSingleIfNotCached(modelName, id, store) {
  return (
    store.peekRecord(modelName, id) ?? (await store.findRecord(modelName, id))
  );
}

export default async function fetchIfNotCached(
  modelName,
  idFilter,
  identifiers,
  store,
) {
  const cachedIdentifiers = store.peekAll(modelName).map((model) => model.id);

  const uncachedIdentifiers = identifiers.filter(
    (identifier) => !cachedIdentifiers.includes(String(identifier)),
  );

  if (uncachedIdentifiers.length) {
    await store.query(modelName, {
      [idFilter]: String(uncachedIdentifiers),
    });
  }

  return store.peekAll(modelName);
}
