import { saveHostName } from "./features/storage";
import submitDetect from "./submit_Detect";
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
        submitDetect();
    }
}

main();
