# Django Svelte Demo Svelte Project

This is very nearly a default Vite + Svelte deployment which can be gotten by "running `npm create vite@latest` and selecting the `svelte` option".([docs](https://svelte.dev/docs/introduction#start-a-new-project-alternatives-to-sveltekit)) The changes made to that default project are thus:
* Added components and such to the `src/components` and `src/lib` directories,
* Added entrypoints to the `src/` directory,
* Added the `build` key to the `defineConfig` in `vite.config.js` with the following config:

```js
export default defineConfig({
  build: {
    rollupOptions: {
      input: [
        'src/App.js',
        'src/AuthComponent.js',
        'src/PostComponent.js'
      ],  // change these out for your own components!
    },
    manifest: true,  // need this so that Django Svelte can locate hashed files
  },
  plugins: [svelte()],
})
```


