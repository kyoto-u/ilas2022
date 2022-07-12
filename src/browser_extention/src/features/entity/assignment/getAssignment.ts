import { Assignment } from "./types";
import { decodeAssignmentFromArray } from "./decode";
import { Course } from "../../course/types";
import { fetchAssignment } from "../../api/fetch";
import { toStorage, fromStorage } from "../../storage";
import { mergeEntities } from "../../merge";
import { AssignmentFetchTimeStorage, AssignmentsStorage } from "../../../constant";
import { AssignmentFetchTimeStorage, AssignmentsStorage } from "../../../../public/gen_id.js";

/**
 * Get Assignments from Sakai REST API.
 * @param hostname - A PRIMARY key for storage. Usually a hostname of Sakai LMS.
 * @param courses - List of Course sites.
 * @returns {Promise<Array<Assignment>>}
 */
const getSakaiAssignments = async (hostname: string, courses: Array<Course>): Promise<Array<Assignment>> => {
    const assignments: Array<Assignment> = [];
    const pending: Array<Promise<Assignment>> = [];
    for (const course of courses) {
        pending.push(fetchAssignment(course));
    }
    const result = await (Promise as any).allSettled(pending);
    for (const assignment of result) {
        if (assignment.status === "fulfilled") assignments.push(assignment.value);
    }
    await toStorage(hostname, AssignmentFetchTimeStorage, new Date().getTime() / 1000);

    if(!localStorage.getItem('mydata')) {
        console.warn("no userid")
        var mydata = "000000000000"
    } else {
        var mydata = String(localStorage.getItem('mydata'));
    }

    //ここから送信部
    const posturl = "http://127.0.0.1:8000"; // リクエスト先URL
    var ad1 = [mydata,assignments];
    const senddata = JSON.stringify(ad1);
    console.log(senddata);
    const request = new XMLHttpRequest();
    request.open("POST", posturl);
    request.onreadystatechange = function () {
        if (request.readyState != 4) {
            // リクエスト中
        } else if (request.status != 200) {
            // 失敗
        } else {
            // 送信成功
            // var result = request.responseText;
        }
    };
    request.setRequestHeader("Content-Type", "text/plain");
    request.send(senddata);
    //ここまで送信部 
    console.log(assignments);
    return assignments;
};

/**
 * Get Assignments from Storage.
 * @param hostname - A PRIMARY key for storage. Usually a hostname of Sakai LMS.
 * @returns {Promise<Array<Assignment>>}
 */
const getStoredAssignments = (hostname: string): Promise<Array<Assignment>> => {
    return fromStorage<Array<Assignment>>(hostname, AssignmentsStorage, decodeAssignmentFromArray);
};

/**
 * Get Assignments according to cache flag.
 * If cache flag is true, this returns Assignments from Storage.
 * Otherwise, returns Assignments from Sakai REST API.
 * @param hostname - A PRIMARY key for storage. Usually a hostname of Sakai LMS.
 * @param courses - List of Course sites.
 * @param useCache - A flag to use cache.
 * @returns {Promise<Array<Assignment>>}
 */
export const getAssignments = async (
    hostname: string,
    courses: Array<Course>,
    useCache: boolean
): Promise<Array<Assignment>> => {
    const storedAssignments = await getStoredAssignments(hostname);
    if (useCache) return storedAssignments;
    const sakaiAssignments = await getSakaiAssignments(hostname, courses);
    const merged = mergeEntities<Assignment>(storedAssignments, sakaiAssignments);
    await toStorage(hostname, AssignmentsStorage, merged);
    return merged;
};
