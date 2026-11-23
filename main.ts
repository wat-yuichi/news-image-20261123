/**
 * make.fun entry point — news-image-20261123.
 *
 * The deliverable is a single picture, entry.png, drawn beforehand by
 * tools/generate_image.py (a newspaper front page for Monday,
 * 23 November 2026).  This program's only job is to place that exact
 * file into the directory the runner points at, unchanged, and to
 * print a one-line receipt describing what was delivered.
 *
 * Run it with:  bun run main.ts   (or: npx tsx main.ts)
 * The runner may set MAKEFUN_OUTPUT_DIR; without it, ./output is used.
 */

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  console.error(
    "entry.png is missing next to main.ts — regenerate it first: " +
      "python3 tools/generate_image.py",
  );
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "output");
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(source, target);

const { size } = statSync(target);
if (size > 1_048_576) {
  console.error(`delivered file is ${size} bytes, over the 1 MiB cap`);
  process.exit(1);
}

console.log(
  `delivered entry.png -> ${target} (${size} bytes, within the 1 MiB cap)`,
);
