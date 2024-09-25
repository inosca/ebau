import { checkbox, input, Separator } from "@inquirer/prompts";
import { execa } from "execa";
import chalk from "chalk";

async function scanImage(image, tag, severity) {
  const fullImageName = `acr.run/camac-ng/camac-ng/${image}:${tag}`;

  await execa(
    "trivy",
    [
      "image",
      `--severity=${severity.join(",")}`,
      "--scanners=vuln",
      "--ignore-unfixed",
      "--exit-code=0",
      "--quiet",
      fullImageName,
    ],
    { stdio: "inherit" },
  );
}

try {
  await execa("which", ["trivy"]);
} catch {
  console.log(
    chalk.bold.red(
      "trivy is not installed. Please install it using this guide: https://aquasecurity.github.io/trivy/v0.55/getting-started/installation/",
    ),
  );
  process.exit(1);
}

const images = await checkbox({
  message: "Select images to scan",
  pageSize: 10,
  choices: [
    { value: "django", checked: true },
    { value: "document-merge-service", checked: true },
    { value: "ember-caluma-portal", checked: true },
    { value: "ember-ebau", checked: true },
    { value: "keycloak", checked: true },
    new Separator("--- Legacy images ---"),
    { value: "db" },
    { value: "ember" },
    { value: "ember-camac-ng" },
    { value: "php" },
  ],
});

const tag = await input({
  message: "Enter image tag",
  default: "master",
  required: true,
});

const severity = await checkbox({
  message: "Select severity levels",
  required: true,
  choices: [
    { value: "CRITICAL", checked: true },
    { value: "HIGH" },
    { value: "MEDIUM" },
    { value: "LOW" },
    { value: "UNKNOWN" },
  ],
});

await execa("trivy", ["image", "--download-db-only", "--no-progress"]);
await Promise.all(images.map((image) => scanImage(image, tag, severity)));
