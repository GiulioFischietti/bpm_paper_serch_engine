import { writable } from "svelte/store";

const urlString = writable(new URL("http://undefined.undefined/"));

export { urlString };
