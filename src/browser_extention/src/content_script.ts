import { saveHostName } from "./features/storage";
import { createMiniSakai } from "./minisakai";
import { isLoggedIn } from "./utils";

/**
 * Creates miniSakai.
 */
async function main() {
    if (isLoggedIn()) {
        const hostname = window.location.hostname;
        createMiniSakai(hostname);
        await saveHostName(hostname);
    }
}

main();
