import { saveHostName } from "./features/storage";
import { createMiniSakai, addMiniSakaiBtn } from "./minisakai";
import submitDetect from "./submit_Detect";
import { isLoggedIn, miniSakaiReady } from "./utils";

/**
 * Creates miniSakai.
 */
async function main() {
    if (isLoggedIn()) {
        addMiniSakaiBtn();
        const hostname = window.location.hostname;
        createMiniSakai(hostname);

        miniSakaiReady();
        await saveHostName(hostname);
        submitDetect();
    }
}

main();
