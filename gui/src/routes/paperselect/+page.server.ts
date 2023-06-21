import { env } from "$env/dynamic/private";
import type { PageServerLoad } from "./$types.js";

export function load(): PageServerLoad {
  return JSON.parse(`{ "pyApi": "${env.PYTHON_APIS}" }`);
}
