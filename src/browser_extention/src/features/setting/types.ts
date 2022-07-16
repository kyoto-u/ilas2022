import { CurrentTime, VERSION } from "../../constant";

type AppInfo = {
    version: string;
    hostname: string;
    currentTime: number;
    useDarkTheme: boolean;
};

export type FetchTime = {
    assignment: number | undefined;
};

type CacheInterval = {
    assignment: number;
};

type DisplayOption = {
    showCompletedEntry: boolean;
    showLateAcceptedEntry: boolean;
};

export class Settings {
    appInfo: AppInfo = {
        version: VERSION,
        hostname: window.location.hostname,
        currentTime: CurrentTime,
        useDarkTheme: false
    };
    fetchTime: FetchTime = {
        assignment: undefined,
    };
    cacheInterval: CacheInterval = {
        assignment: 120,
    };
    miniSakaiOption: DisplayOption = {
        showCompletedEntry: true,
        showLateAcceptedEntry: false
    };

    setFetchtime(fetchTime: FetchTime) {
        this.fetchTime = fetchTime;
    }
}
