import { extract } from "../lib/link-checker.js";
import { createObjectCsvWriter } from "csv-writer";

const csvWriter = createObjectCsvWriter({
  path: "be-links.csv",
  header: [{ id: "link", title: "Link" }],
});

async function run() {
  const links = extract();

  const rows = [
    ...new Set(
      links
        .map(([_, link]) => link)
        .filter((link) => /http(s)?:\/\/.*be.ch\//.test(link))
    ),
  ]
    .sort()
    .map((link) => ({ link }));

  await csvWriter.writeRecords(rows);
}

run();
