import { env } from "$env/dynamic/private";

export function load({}) {
  return { host: env.PYTHON_APIS };
}
