import { env } from "$env/dynamic/private";

export function load({ url }) {
  const queryString = decodeURIComponent(url.searchParams?.get("query") ?? "");
  console.log(queryString);
  return { host: env.PYTHON_APIS, queryString };
}
