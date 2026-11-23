import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourceImage = join(import.meta.dirname, "entry.png");

if (!existsSync(sourceImage)) {
  throw new Error("Bundled news image is missing");
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, join(outputDir, "entry.png"));
