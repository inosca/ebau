import { extract, config } from "../lib/link-checker.js";
import { createObjectCsvWriter } from "csv-writer";

const csvWriter = createObjectCsvWriter({
  path: "be-links.csv",
  header: [
    { id: "link", title: "Link" },
    { id: "label", title: "Frage" },
    { id: "infoText", title: "Infotext" },
  ],
});

async function run() {
  const links = extract();

  const rows = links
    // remove duplicates
    .filter(
      ([pk, link], index) => index === links.findIndex((l) => l[1] === link)
    )
    .filter(([pk, link]) => /http(s)?:\/\/.*be.ch\//.test(link))
    .sort(([_, linkA], [__, linkB]) => (linkA > linkB ? 1 : -1))
    .map(([pk, link]) => ({ link, ...details(pk) }));

  await csvWriter.writeRecords(rows);
}

function details(questionPk) {
  const { fields } = config.find(
    (obj) => obj.model === "caluma_form.question" && obj.pk === questionPk
  );
  return {
    label: JSON.parse(fields.label).de,
    infoText: JSON.parse(fields.info_text).de,
  };
}

run();
