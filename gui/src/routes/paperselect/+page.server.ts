import { error } from "@sveltejs/kit";

export async function load({ url }) {
  console.log("you queried: ", url.searchParams.get("query"));
}
