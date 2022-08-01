import { FetchTime, Settings } from "./features/setting/types";
import { Course } from "./features/course/types";
import { Assignment } from "./features/entity/assignment/types";
import { getAssignments } from "./features/entity/assignment/getAssignment";
import { fromStorage } from "./features/storage";
import { AssignmentFetchTimeStorage, MaxTimestamp } from "./constant";
import { EntryProtocol } from "./features/entity/type";

export type DueCategory = "due24h" | "due5d" | "due14d" | "dueOver14d" | "duePassed";

/**
 * Fetch entities for miniSakai.
 * @param settings - Settings for miniSakai.
 * @param courses - List of Course sites.
 * @param cacheOnly - A flag to force use cache.
 */
export async function getEntities(settings: Settings, courses: Array<Course>, cacheOnly = false) {
    const hostname = settings.appInfo.hostname;
    const currentTime = settings.appInfo.currentTime;
    const fetchTime = await getFetchTime(hostname);
    const assignment: Array<Assignment> = await getAssignments(
        hostname,
        courses,
        cacheOnly || shouldUseCache(fetchTime.assignment, currentTime, settings.cacheInterval.assignment)
    );
    return {
        assignment: assignment
    };
}

/**
 * Decoder for timestamp.
 * @param data - Target value
 * @returns {number | undefined}
 */
const decodeTimestamp = (data: any): number | undefined => {
    if (data === undefined) return undefined;
    return data as number;
};

/**
 * Decides whether to use cache or not according to last fetched time.
 * @param fetchTime - Last fetched timestamp
 * @param currentTime - Current timestamp
 * @param cacheInterval - User-configured cache time-interval
 * @returns {boolean}
 */
export const shouldUseCache = (fetchTime: number | undefined, currentTime: number, cacheInterval: number): boolean => {
    if (fetchTime === undefined) return false;
    return currentTime - fetchTime <= cacheInterval;
};

/**
 * Get last fetched time from Storage.
 * @param hostname - A PRIMARY key for storage. Usually a hostname of Sakai LMS.
 * @returns {Promise<FetchTime>>}
 */
export async function getFetchTime(hostname: string): Promise<FetchTime> {
    const assignmentTime = await fromStorage<number | undefined>(hostname, AssignmentFetchTimeStorage, decodeTimestamp);
    return {
        assignment: assignmentTime,
    };
}

/**
 * Calculate category of due date according to days until due.
 * @param {number} dt1 Current timestamp
 * @param {number} dt2 Target timestamp
 * @returns {DueCategory}
 */
function getDaysUntil(dt1: number, dt2: number): DueCategory {
    let diff = dt2 - dt1;
    diff /= 3600 * 24;
    let category: DueCategory;
    if (diff > 0 && diff <= 1) {
        category = "due24h";
    } else if (diff > 1 && diff <= 5) {
        category = "due5d";
    } else if (diff > 5 && diff <= 14) {
        category = "due14d";
    } else if (diff > 14) {
        category = "dueOver14d";
    } else {
        category = "duePassed";
    }
    return category;
}

/**
 * Format timestamp for miniSakai.
 * @param {number | undefined} timestamp - Target timestamp
 * @returns {string}
 */
function formatTimestamp(timestamp: number | undefined): string {
    if (timestamp === undefined) return "---";
    const date = new Date(timestamp * 1000);
    return (
        date.toLocaleDateString() +
        " " +
        date.getHours() +
        ":" +
        ("00" + date.getMinutes()).slice(-2) +
        ":" +
        ("00" + date.getSeconds()).slice(-2)
    );
}

/**
 * Get the closest timestamp of given Entries.
 * @param settings - Settings for miniSakai.
 * @param entries - Entries of each Entity.
 */
export const getClosestTime = (settings: Settings, entries: Array<EntryProtocol>): number => {
    const option = settings.miniSakaiOption;
    const appInfo = settings.appInfo;
    return entries
        .filter((e) => {
            // Check if user chose to hide completed Entry
            if (!option.showCompletedEntry) {
                // Skip if the Entry is completed
                if (e.hasFinished) return false;
            }
            return settings.appInfo.currentTime <= e.getTimestamp(appInfo.currentTime, option.showLateAcceptedEntry);
        })
        .reduce(
            (prev, e) => Math.min(e.getTimestamp(appInfo.currentTime, option.showLateAcceptedEntry), prev),
            MaxTimestamp
        );
};

/**
 * Get script tag.
 * @returns {Array<HTMLScriptElement>}
 */
export const getScripts = (): Array<HTMLScriptElement> => {
    return Array.from(document.getElementsByTagName("script"));
};

/**
 * Check if user is logged-in to Sakai LMS.
 */
function isLoggedIn(): boolean {
    const scripts = getScripts();
    let loggedIn = false;
    for (const script of scripts) {
        if (script.text.match("\"loggedIn\": true")) loggedIn = true;
    }
    return loggedIn;
}

/**
 * Get Course site ID of current page.
 * @param currentHref - Current href.
 * @returns {string | undefined}
 */
export const getCourseSiteID = (currentHref: string): string | undefined => {
    let courseID: string | undefined;
    const reg = new RegExp("(https?://[^/]+)/portal/site/([^/]+)");
    if (currentHref.match(reg)) {
        courseID = currentHref.match(reg)?.[2];
    }
    return courseID;
};

/**
 * Changes miniSakai loading state to ready state.
 */
function miniSakaiReady(): void {
    const loadingIcon = document.getElementsByClassName("cs-loading")[0];
}

/**
 * Create date string for miniSakai.
 * @param seconds - Target timestamp.
 * @returns {string}
 */
export function createDateString(seconds: number | null | undefined): string {
    if (seconds === MaxTimestamp || seconds === undefined || seconds === null) return "----/--/--";
    const date = new Date(seconds * 1000);
    return date.toLocaleDateString() + " " + date.getHours() + ":" + ("00" + date.getMinutes()).slice(-2);
}

export { getDaysUntil, formatTimestamp, isLoggedIn, miniSakaiReady };
