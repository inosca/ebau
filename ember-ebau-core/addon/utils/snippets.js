export function groupAndSort(records) {
  const recordsArray = records.toArray ? records.toArray() : records;
  const categories = new Set(recordsArray.map((s) => s.purpose));

  return [...categories].toSorted().reduce((grouped, purpose) => {
    return {
      ...grouped,
      [purpose]: recordsArray
        .filter((s) => s.purpose === purpose)
        .toSorted((a, b) => a.subject.localeCompare(b.subject)),
    };
  }, {});
}
