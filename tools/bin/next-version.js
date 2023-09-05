import { select, confirm, checkbox } from "@inquirer/prompts";
import { execa } from "execa";
import calver from "calver";
import chalk from "chalk";
import yargs from "yargs";
import { hideBin } from "yargs/helpers";

const warn = chalk.bold.hex("#FFA500");
const error = chalk.bold.red;
const success = chalk.bold.green;

const argv = yargs(hideBin(process.argv)).argv;

function cleanVersion(version, canton) {
  return version.replace(new RegExp(`^${canton}-v`), "");
}

async function getLatest(canton, limit = 10) {
  try {
    const { stdout } = await execa("git", [
      "tag",
      "-l",
      "--sort=-creatordate",
      "n",
      `${canton}-v*`,
    ]);

    const versions = stdout.split("\n");

    return versions.slice(0, limit);
  } catch (e) {
    console.log("no latest", e);
    return [];
  }
}

const canton =
  argv.canton ??
  (await select({
    message: "Select a canton",
    choices: [
      { value: "be", name: "Bern" },
      { value: "gr", name: "Graubünden" },
      { value: "so", name: "Solothurn" },
      { value: "sz", name: "Schwyz" },
      { value: "ur", name: "Uri" },
    ],
  }));

const latest10 = await getLatest(canton);
let latest = latest10[0];

if (latest) {
  const correctLatest = await confirm({
    message: `Is "${latest}" the latest version?`,
  });

  if (!correctLatest) {
    latest = await select({
      message: "Please select the latest version",
      choices: latest10.map((version) => ({ value: version })),
      pageSize: 10,
    });
  }
}

if (!latest) {
  console.log(warn("No latest version found"));
}

const typesFromArgs = [
  ...(argv.minor ? ["minor"] : []),
  ...(argv.patch ? ["patch"] : []),
  ...(argv.rc ? ["rc"] : []),
];

const types = typesFromArgs.length
  ? typesFromArgs
  : await checkbox({
      message: "Select a release type",
      choices: [
        { value: "minor", name: "Minor" },
        { value: "patch", name: "Patch (bugfixes only)" },
        { value: "rc", name: "Release candidate (staging only)" },
      ],
    });

const calverLevel = ["calendar", ...types].join(".");

try {
  const nextVersion = calver.inc(
    "yy.minor.patch",
    latest ? cleanVersion(latest, canton) : "",
    calverLevel,
  );

  const fullVersion = `${canton}-v${nextVersion}`;
  console.log(success(`Next version is: ${fullVersion}`));

  console.log(
    `https://git.adfinis.com/camac-ng/camac-ng/-/tags/new?tag_name=${fullVersion}`,
  );
} catch (e) {
  console.log(error("Next version could not be determined"));
  console.log(e);
}
