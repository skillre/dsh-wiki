#!/usr/bin/env node
/**
 * dsh-wiki-init <vault-path>
 *
 * Initializes a wiki vault directory with the dsh-wiki resources:
 *   <vault>/.dsh/skills/   5 wiki skills (project-level discovery)
 *   <vault>/.dsh/scripts/  gen-index.py + maintain.py
 *   <vault>/templates/     note-template.md
 *
 * Usage:
 *   npx dsh-wiki-init ~/mywiki
 *   dsh-wiki-init ~/mywiki          (npm global install)
 *   node <path-to>/init.js ~/mywiki (tarball / local checkout)
 *
 * Vault path defaults to the current working directory when omitted.
 */

import { cpSync, existsSync, mkdirSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
// init.js lives at the package root, next to skills/ scripts/ templates/,
// both in a local checkout and under node_modules/dsh-wiki/.
const pkgRoot = here

const RESOURCES = ['skills', 'scripts', 'templates']

function main() {
  const raw = process.argv.slice(2).filter((a) => !a.startsWith('-'))
  if (raw.length > 1) {
    console.error('usage: dsh-wiki-init [vault-path]')
    process.exit(1)
  }
  const vault = resolve(raw[0] || process.cwd())

  for (const res of RESOURCES) {
    const src = join(pkgRoot, res)
    if (!existsSync(src)) {
      console.error(`dsh-wiki: missing resource ${src} — is this the dsh-wiki package?`)
      process.exit(1)
    }
    const dest = res === 'skills' ? join(vault, '.dsh', 'skills')
      : res === 'scripts' ? join(vault, '.dsh', 'scripts')
      : join(vault, 'templates')
    mkdirSync(dest, { recursive: true })
    cpSync(src, dest, { recursive: true })
  }

  console.log(`dsh-wiki initialized in ${vault}`)
  console.log('  .dsh/skills/   5 wiki skills (visible in DSH sessions rooted at this vault)')
  console.log('  .dsh/scripts/  gen-index.py + maintain.py (auto-detect vault root)')
  console.log('  templates/     note-template.md')
  console.log('Next: open the folder as an Obsidian vault, add it as a DSH workspace, done.')
}

main()
