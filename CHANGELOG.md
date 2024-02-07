# Changelog

## Version 0.2.0
### Added
* This changelog!
* Demo project into this package illustrating working Svelte 4 deployment.
* Unittests!
* Setting `DJANGO_SVELTE_VITE_MANIFEST_PATH` which locates the Vite build manifest so that hashed files can be looked up.
* Setting `DJANGO_SVELTE_ENTRYPOINT_PREFIX` with default (`src/`) to indicate the directory of the Svelte entrypoint files (formerly referred to like `main-<componentname>.js`, now format like `<ComponentName>.js` is preferred)
* Setting `DJANGO_SVELTE_VITE_ASSETSDIR` with default (`assets/`) to indicate the directory where Vite will output the various bundles for reference.
* Support for looking up hashed file names from the Vite manifest.
### Changed
* Handling of CSS to dedicated templatetag which can appropriately be invoked in the `head` of the template.
* Documentation to speak more directly to handling CSS in the two most common use cases.
