---
name: mytui-art
description: >-
  Generate and configure custom ASCII art for the opencode TUI mytui plugin. Use this skill whenever
  the user mentions customizing or changing the ASCII art, logo, sidebar art, or text banner in their
  opencode terminal UI. Also trigger when the user wants a new look, mentions "mytui customization",
  or asks to replace the OPENCODE logo with their own text. This skill handles ASCII art generation
  and writes the art files into the user's config directory.
---

# mytui Custom ASCII Art

Configure custom ASCII art for the `@forget2save/mytui` opencode TUI plugin. The plugin loads art
from the user's config directory at runtime — files placed there override the default art without
any config changes.

## File locations

| File | Purpose |
|------|---------|
| `~/.config/opencode/mytui/home.txt` | Home screen logo (replaces "OPENCODE") |
| `~/.config/opencode/mytui/side.txt` | Sidebar art (replaces pipboy) |

Both files: one row of ASCII art per line. No blank lines at the end.

## Generating art

### Primary: generate art programmatically (most reliable)

The user's text must be converted to ASCII art. Do NOT try to web-scrape patorjk.com — it renders
client-side and cannot be fetched. Instead, generate the art directly:

1. Check if `figlet` is available via npm:
   ```bash
   npx figlet "ZHU CODE" -f Bloody
   ```
   If `figlet` is not installed or the font is missing, install it:
   ```bash
   npm install -g figlet
   ```
   Run `figlet -l` to list available fonts, then use any font the user likes.

2. If figlet fails, use `pyfiglet` (Python):
   ```bash
   pip install pyfiglet && pyfiglet "ZHU CODE" -f bloody
   ```

3. If neither works, generate art manually by writing each character row-by-row using a known
   figlet font mapping or by building a simple character-height block render in code.

4. Save the output to a file, then process it: remove trailing empty lines, ensure all rows have
   the same length (pad shorter rows with trailing spaces).

### Browser automation (if agent-browser skill is available)

1. Navigate to https://patorjk.com/software/taag/
2. Type the desired text into the input field
3. Select a font from the dropdown
4. Copy the output text area

### User-provided art

The user may paste art directly. Accept it as-is — the plugin handles variable widths.

## Writing the files

After obtaining the art, write it to the appropriate config file.

### Home screen (home.txt)

- Each line is one row of the logo
- The `█` character creates "solid" blocks that spawn animated water droplets
- The `░` character is rendered as transparent (empty space)
- Other characters get the rainbow gradient

### Sidebar (side.txt)

- Each line is one row of the art
- Spaces and `⠀` (braille blank) are transparent
- All other characters get the animated hue gradient

### Windows users

On Windows, the config path is `%USERPROFILE%\.config\opencode\mytui\`. Use backslashes with
PowerShell, or forward slashes with Node.js `fs`.

## Verification

1. Ensure the directory `~/.config/opencode/mytui/` exists (create it if not)
2. Write the file(s) using the Write tool
3. Tell the user to restart opencode to see changes
4. If issues: check line endings are `\n` (LF), not `\r\n` (CRLF)
5. Each line of art must have the same width (pad shorter lines with trailing spaces)
