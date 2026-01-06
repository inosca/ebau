import { select, confirm, checkbox } from "@inquirer/prompts";
import { execa } from "execa";
import calver from "calver";
import chalk from "chalk";

const warn = chalk.bold.hex("#FFA500");
const error = chalk.bold.red;
const success = chalk.bold.green;

function cleanVersion(version, canton) {
  return version.replace(new RegExp(`^${canton}-v`), "");
}

function isReleaseCandidate(version) {
  return /-rc\.\d+$/.test(version);
}

function removeReleaseCandidate(version) {
  return version.replace(/-rc\.\d+$/, "");
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

const canton = await select({
  message: "Select a canton",
  choices: [
    { value: "be", name: "Bern (SemVer)", disabled: true },
    { value: "gr", name: "Graubünden (branches)", disabled: true },
    { value: "so", name: "Solothurn" },
    { value: "sz", name: "Schwyz" },
    { value: "ur", name: "Uri (branches)", disabled: true },
    { value: "ag", name: "Aargau" },
  ],
});

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

let version = cleanVersion(latest ?? "", canton);

let types = await checkbox({
  message: "Select a release type",
  choices: [
    {
      value: "calendar.minor",
      name: "Minor",
      description:
        "Regular feature release. Can be combined with release candidate.",
    },
    {
      value: "calendar.patch",
      name: "Patch (bugfixes only)",
      description:
        "Bugfix release (commonly known as hotfix). Can be combined with release candidate",
    },
    {
      value: "rc",
      name: "Release candidate",
      description:
        "Release candidate, for testing environments only. If selected without combination with minor or patch, the existing RC version will be bumped.",
    },
    ...(isReleaseCandidate(version)
      ? [
          {
            value: "calendar",
            name: "Promote release candidate",
            description: "Removes the RC suffix from the latest version.",
          },
        ]
      : []),
  ],
  shortcuts: {
    all: null,
    invert: null,
  },
  required: true,
  validate: (items) => {
    const values = items.map((i) => i.value);

    if (
      values.includes("calendar.minor") &&
      values.includes("calendar.patch")
    ) {
      return "Minor and patch can't be combined";
    }

    if (values.includes("calendar") && values.length > 1) {
      return "Promotion of release candidate can't be combined with other release types";
    }

    return true;
  },
});

if (types.includes("rc") && types.length > 1) {
  // If we combine rc with minor or mayor but the latest version already
  // contains an rc number, it would increase the rc number while also bumping
  // the minor / patch version which doesn't make sense for our use-case.
  // To avoid this behaviour, we simply remove the rc version for that case.
  version = removeReleaseCandidate(version);
}

try {
  const nextVersion = calver.inc("yy.minor.patch", version, types.join("."));

  const fullVersion = `${canton}-v${nextVersion}`;
  console.log(success(`Next version is: ${fullVersion}`));

  console.log(
    `https://git.adfinis.com/camac-ng/camac-ng/-/tags/new?tag_name=${fullVersion}`,
  );
} catch (e) {
  console.log(error("Next version could not be determined"));
  console.log(e);
}
