import React from "react";
import { createRoot } from "react-dom/client";
import { MiniSakaiRoot } from "./components/main";

/**
 * Change visibility of miniSakai.
 */
export const miniSakai = document.createElement("div");
miniSakai.id = "miniSakai";
miniSakai.classList.add("cs-minisakai", "cs-tab");

/**
 * Insert miniSakai into Sakai LMS.
 * @param hostname - A PRIMARY key for storage. Usually a hostname of Sakai LMS.
 */
export function createMiniSakai(hostname: string) {
    const root = createRoot(miniSakai);
    root.render(<MiniSakaiRoot subset={false} hostname={hostname} />);
}
