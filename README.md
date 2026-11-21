# Regency Foods — design archive

Everything produced for the Regency Foods brand and site redesign, saved here so it
survives the chat it was made in.

The live store is **regencyfoods.com**, a BigCommerce storefront on a Stencil theme.
The work here is a redesign of that storefront. The existing catalogue stays as it is;
only the design changes.

## What's in here

| Folder | Contents |
| --- | --- |
| `website/current-redesign/` | The latest site: `index.html`, `styles.css`, `app.js` |
| `website/earlier-versions/` | Two earlier generations, `v1` oldest |
| `website/walkthrough-pages/` | Standalone pages used for the walkthrough films |
| `website/regency-foods-final.zip` | An earlier full site bundle, with its own image assets |
| `packaging/blender/` | `scene.py` — the Blender scene that renders every pack shot |
| `packaging/renders/` | Pack mockups: hero, pile, row, flat lay, window macro |
| `packaging/source-photography/` | The nut photography behind the pack windows |
| `film/` | Pack spin and homepage films |
| `brand/` | Brand guidelines and the two brand typefaces |
| `scripts/` | Generators for the imagery and page layouts |
| `reference/` | Screenshots and reference images gathered along the way |

## Which version is current

Three generations of `index.html` / `styles.css` / `app.js` exist. They were matched up
by checking every CSS class used in each HTML against the classes each stylesheet
defines, and every DOM reference in each `app.js` against each HTML. The newest set
matches 107 of 107 classes; the pairings are recorded in the folder names.

**One gap worth knowing about:** `website/current-redesign/` references 15 images
(`assets/img/van.jpg`, `hero-stack.jpg`, `bag-*.jpg` and others) that are not in this
archive — they were generated in a working session and only the code came back. The
scripts in `scripts/` are what produced them. The zip holds an earlier, complete set of
assets under different filenames.

## Rebuilding the pack renders

`packaging/blender/scene.py` is self-contained. In Blender's Python console:

```python
SCENE='hero'; FINAL=True; exec(open('/path/to/scene.py').read())
```

`SCENE` accepts `hero`, `pile`, `spin`, `shot_low`, `shot_row`, `shot_trio`,
`shot_macro`. Without `FINAL=True` it renders a fast preview. It expects the pack
artwork in a `tex/` folder beside it, which is not in this archive.
