Got it! Here's the updated `README.md` with that detail corrected:

---

```markdown
# Quicknode

Quicknode is a lightweight custom tab for **Katana**, designed to speed up your node-based workflow. It offers quick access to frequently used node setups and integrates seamlessly with **3Delight**.

## Features

- Custom tab integration for Katana.
- Streamlined creation of common node structures.
- Ready for use with 3Delight renderer.

## Installation

1. Clone or download this repository.

2. Locate your `.katana` directory (usually in your home folder).  
   The `.katana` folder should already exist if you've run Katana before.

3. Inside `.katana`, ensure a `Tabs` directory exists. If not, create it:

   ```bash
   mkdir -p ~/.katana/Tabs
   ```

4. Copy the `Quicknode` folder into the `Tabs` directory:

   ```bash
   cp -r Quicknode ~/.katana/Tabs/
   ```

Katana will load the **Quicknode** tab the next time it launches.

## Requirements

- **Katana** (Tested with current versions)
- **3Delight** installed at: `/home/bas/3delight-2.9.128`  
  *(Modify any hardcoded paths in the script if needed)*

## Usage

After starting Katana, find the **Quicknode** tab in the UI. Use it to insert common node templates and accelerate your scene-building process.

## License

MIT

---

Feel free to contribute or submit feedback!
```

Let me know if Quicknode should support any other renderers or have config options, and I can expand it.
