import { writable } from "svelte/store";

export const username = writable("")
export const isGuest = writable(true)