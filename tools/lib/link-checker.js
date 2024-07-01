import MarkdownIt from "markdown-it";
import fetch from "node-fetch";
import { readFileSync } from "fs";
import { globSync } from "glob";

const paths = globSync("../django/kt_bern/config/caluma_*form*.json");

export const config = paths.reduce(
  (all, path) => [...all, ...JSON.parse(readFileSync(path))],
  [],
);

export function extract() {
  return config
    .filter((obj) => obj.model === "caluma_form.question")
    .map((q) => [q.pk, q.fields.info_text])
    .map(([pk, info]) => [pk, JSON.parse(info)])
    .reduce((res, [pk, { de, fr }]) => {
      return [...res, [pk, de], [pk, fr]];
    }, [])
    .filter(([pk, link]) => !!link)
    .map(([pk, link]) => [pk, getLinksFromMarkdown(link)])
    .reduce((res, [pk, links]) => {
      return [...res, ...links.map((link) => [pk, link])];
    }, []);
}

export async function checkLink(url) {
  if (!/^https?:\/\//i.test(url)) {
    // relative links should not be checked
    return true;
  }

  try {
    const response = await fetch(url);

    return response.ok;
  } catch (error) {
    return false;
  }
}

export function getLinksFromMarkdown(text) {
  const ast = MarkdownIt().parse(text, {});

  return ast.reduce((res, token) => {
    return [...res, ...extractLinks(token)];
  }, []);
}

export function extractLinks(token) {
  const links = token.children
    ? token.children.reduce((res, token) => {
        return [...res, ...extractLinks(token)];
      }, [])
    : [];

  if (token.type === "link_open") {
    links.push(token.attrs[0][1]);
  }
  return links;
}
