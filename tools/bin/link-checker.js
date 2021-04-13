import { checkLink, extract } from "../lib/link-checker.js";
import { createObjectCsvWriter } from "csv-writer";

const csvWriter = createObjectCsvWriter({
  path: "result.csv",
  header: [
    { id: "pk", title: "Frage" },
    { id: "link", title: "Link" },
    { id: "status", title: "Status" },
  ],
});

async function run() {
  const links = extract();
  console.log(`checking ${links.length} links ...`);

  const rows = [];
  for (let [pk, link] of links) {
    console.log(`checking ${link} ... `);
    const res = await checkLink(link);
    rows.push({ pk, link, status: res ? "OK" : "NOK" });
  }

  const errors = rows.filter((row) => row.status === "NOK");

  if (!errors.length) {
    console.log("Congratulations! All Links seem to work!");
    return;
  }

  console.log(`${errors.length} links don't work :(`);
  await csvWriter.writeRecords(errors);
  console.log("Results written to 'result.csv'");
}

run();
