import fs from 'fs';
import chalk from 'chalk';
import prettyjson, { render } from 'prettyjson';

const args = process.argv.slice(2);

if (args.length !== 2) {
  console.error('Usage: node compare-dumps.js <dump1> <dump2>');
}

const file1 = JSON.parse(fs.readFileSync(args[0], 'utf8'));
const file2 = JSON.parse(fs.readFileSync(args[1], 'utf8'));

function compareObjects(obj1, obj2) {
  const keys1 = Object.keys(obj1 ?? {});
  const keys2 = Object.keys(obj2 ?? {});
  const allKeys = new Set([...keys1, ...keys2]);

  const differences = {};

  for (const key of allKeys) {
    if (typeof obj1[key] === 'object' && typeof obj2[key] === 'object') {
      const nestedDifferences = compareObjects(obj1[key], obj2[key]);

      if (Object.keys(nestedDifferences).length > 0) {
        differences[key] = nestedDifferences;
      }
    } else if (obj1[key] !== obj2[key]) {
      differences[key] = {
        old: chalk.red(obj1[key]),
        new: chalk.yellowBright(obj2[key]),
      };
    }
  }

  return differences;
}

function renderObj(obj, differences = {}) {
  console.log(prettyjson.render({
    model: chalk.blue.bold(obj.model),
    pk: chalk.cyan.bold(obj.pk),
    ...differences}));
  console.log("\n")
}

const removed = [];
const added = [];

console.log('\n');
console.log(chalk.underline.bold.cyan('Differences:'));

file1.forEach((obj1) => {
  const obj2 = file2.find((obj2) => obj2.model === obj1.model && obj1.pk === obj2.pk)

  if (!obj2) {
    removed.push(obj1);
    return;
  }

  const differences = compareObjects(obj1, obj2);

  if (Object.keys(differences).length > 0) {
    renderObj(obj1, differences)
  }
})

file2.forEach((obj2) => {
  const obj1 = file1.find((obj1) => obj2.model === obj1.model && obj1.pk === obj2.pk)

  if (!obj1) {
    added.push(obj2);
  }
})

function printListOfObjs (title, objs, color) {
  if (objs.length === 0) {
    return
  }

  console.log(chalk.underline.bold[color](title));

  objs.forEach((obj) => {
    const objWithoutModelAndPk = {...obj};
    delete objWithoutModelAndPk.model;
    delete objWithoutModelAndPk.pk;
    renderObj(obj, objWithoutModelAndPk);
  })
}

printListOfObjs("Removed:", removed, 'red');
printListOfObjs("Added:", added, 'green');
