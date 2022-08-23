function instanceReductor(all, workItem) {
  return [
    ...all,
    workItem.case.parentWorkItem?.case.meta["camac-instance-id"] ||
      workItem.case.meta["camac-instance-id"],
  ];
}

function usernameReductor(all, workItem) {
  return [
    ...all,
    ...workItem.assignedUsers,
    workItem.createdByUser,
    workItem.closedByUser,
  ];
}

function serviceReductor(all, workItem) {
  return [
    ...all,
    ...workItem.addressedGroups,
    workItem.createdByGroup,
    workItem.closedByGroup,
  ];
}

async function _fetchIfNotCached(
  store,
  modelName,
  identifiers,
  identifierPropertyName,
  identifierFilterName,
  filters = {}
) {
  if (!identifiers.length) return;

  const cachedIdentifiers = store
    .peekAll(modelName)
    .map((model) => String(model[identifierPropertyName]));

  const uncachedIdentifiers = identifiers.filter(
    (identifier) => !cachedIdentifiers.includes(String(identifier))
  );

  if (!uncachedIdentifiers.length) return;

  return await store.query(modelName, {
    [identifierFilterName]: uncachedIdentifiers.join(","),
    ...filters,
  });
}

export async function processNewWorkItems(store, workItems) {
  const { usernames, instanceIds, serviceIds } = getProcessData(workItems);

  await _fetchIfNotCached(
    store,
    "public-user",
    usernames,
    "username",
    "username"
  );
  await _fetchIfNotCached(store, "instance", instanceIds, "id", "instance_id", {
    include: "form",
  });
  await _fetchIfNotCached(store, "service", serviceIds, "id", "service_id");

  return workItems;
}

export default function getProcessData(workItems) {
  const instanceIds = [...new Set(workItems.reduce(instanceReductor, []))];
  const usernames = [...new Set(workItems.reduce(usernameReductor, []))];
  const serviceIds = [...new Set(workItems.reduce(serviceReductor, []))];

  return {
    instanceIds: instanceIds.filter(Boolean),
    usernames: usernames.filter(Boolean),
    serviceIds: serviceIds.filter((s) => parseInt(s)),
  };
}
