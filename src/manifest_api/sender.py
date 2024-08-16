import json
import logging
import re

from celery import shared_task

from src.manifest_api.get_data import send_request, upload_file, get_steps_by_asset_class
from src.manifest_api.service import sorted_response

logger = logging.getLogger(__name__)


def find_by_operation_name(name, data):
    for item in data:
        if item.get("operationName") == name:
            return item
    return None


@shared_task
def send_manifest_response(extra):
    data_manifest = get_steps_by_asset_class()[0]
    sorted_data = sorted_response(extra)
    for item in sorted_data:
        name_workplace = item.get('name_workplace')

        operations = find_by_operation_name(name_workplace, data_manifest)
        if not operations:
            continue

        asset_class_id = operations.get('asset_class_id')
        asset_id = operations.get('id_asset')
        location_id = operations.get("location_id")
        job_template = item.get("template_id")
        assigned_user = operations.get("creator_by_id")

        job_id = create_job(location_id, assigned_user, job_template, asset_id)

        if not job_id:
            print(f'Could not create job status code {job_id.status_code}, {job_id.message}')
            continue

        for step in item.get('steps'):
            step = step.get('step')
            all_images = step.get('all_images_zones')
            durations = step.get('all_durations')

            start_job_step(job_id, step)
            print("start_job_step job step", step)
            list_id_load_images = []
            for image_path in all_images:
                print(image_path)
                id_image = upload_file(image_path)

                if id_image:
                    list_id_load_images.append(id_image)

            if list_id_load_images:
                print(list_id_load_images)
                added_notes(job_id, step, list_id_load_images)
                print(f"Added notes for step={step}, job_id={job_id}")

            add_durations_job_steep(job_id, durations)
            complete_job_step(job_id, step)
            print("complete_job_step job step", step)

    print("Sending all jobs to manifest")
    logger.info("Sending all jobs to manifest")
    return "success True"
    # except:
    #     return "success False"


def added_notes(job_id, step, list_id_image):
    payload = "{\"query\":\"mutation($notes: [JobNoteInput!]!) {\\n    addNotes(notes: $notes)\\n    }\",\"variables\":{\"notes\":["
    for id_image in list_id_image:
        id = id_image.get("id")
        item = "{\"jobId\":" + f'{job_id}' + ",\"step\":" + f'{step}' + ",\"type\":\"photo\",\"title\":\"st4\",\"text\":\"\",\"files\":" + f'{id}' + "},"
        payload += item
    payload = payload.rstrip(',') + "]}}"

    response, status_code = send_request(payload)
    if status_code != 200:
        return None, status_code
    return


def create_job(location_id, assigned_user_id, job_template, asset_id):
    payload = "{\"query\":\"mutation ($job: JobInput! ) { \\n    addJob (data: $job) \\n    }\",\"variables\":{\"job\":{\"title\":\"test job with 5s\",\"locationId\":" + f"{location_id}" + ",\"priority\":\"2\",\"assignedUserId\":" + f"{assigned_user_id}" + ",\"jobTemplate\":" + f"{job_template}" + ",\"assetId\":" + f"{asset_id}" + "}}}"

    response, status_code = send_request(payload)
    if status_code != 200:
        return None, status_code

    job_id = response.get('data').get('addJob')
    return job_id


def start_job_step(job_id, step):
    payload = "{\"query\":\"mutation($jobId: Int!,$step: Int!) {\\n    startJobStep(jobId: $jobId, step: $step)\\n    }\",\"variables\":{\"jobId\":"f"{job_id}"",\"step\":"f"{step}""}}"
    response, status_code = send_request(payload)
    print("start_job_step status_code", status_code)
    if status_code != 200:
        return [], status_code
    return {"step": "success"}


def complete_job_step(job_id, step):
    payload = "{\"query\":\"mutation (\\n    $jobId: Int!,\\n    $step: Int!,\\n    $completed: Boolean,\\n    $compliant: Boolean,\\n    $supportedEvidence: [String]\\n) {\\n    completeJobStep (\\n        jobId: $jobId,\\n        step: $step,\\n        completed: $completed,\\n        compliant: $compliant,\\n        supportedEvidence: $supportedEvidence\\n    )\\n}\\n\",\"variables\":{\"jobId\":"f"{job_id}"",\"step\":"f"{step}"",\"supportedEvidence\":\"Pen\",\"completed\":true,\"compliant\":true}}"

    response, status_code = send_request(payload)
    print("complete_job_step status_code", status_code)
    if status_code != 200:
        return [], status_code
    return {"complete": "success"}


def get_all_works_manifest():
    result = []
    payload = "{\"query\":\"query(\\n    $assetId: Int,\\n    $assetClassId: Int,\\n    $locationId: Int,\\n    $completed: Boolean,\\n    $itemsPerPage: Int,\\n    $pageNumber: Int,\\n    $filters: JobsFiltersInput,\\n    $orderBy: String,\\n    $reverseOrder: Boolean,\\n    $search: JobSearchInput,\\n    $sort: SortInput\\n) {\\n    jobsPage(\\n        assetId: $assetId,\\n        assetClassId: $assetClassId,\\n        locationId: $locationId,\\n        completed: $completed,\\n        itemsPerPage: $itemsPerPage,\\n        pageNumber: $pageNumber,\\n        filters: $filters,\\n        orderBy: $orderBy,\\n        reverseOrder: $reverseOrder,\\n        search: $search,\\n        sort: $sort\\n    ) {\\n        id\\n        parentJobId\\n        assetId\\n        autoplay\\n        locationId\\n        elapsedTime\\n        completedStepPercent\\n        title\\n        description\\n        priority\\n        externalId\\n        templateId\\n        jobType\\n        creationDate\\n        startDate\\n        completionDate\\n        status\\n        assignedUser\\n        associatedGroupChatId\\n        teamSetupCompleted\\n        workItemType\\n        hasOpenFaults\\n        newJobPromptCancelled\\n        faults {\\n            id\\n            resolvedAt\\n            description\\n            createdByUserId\\n            jobStepId\\n        }\\n        asset {\\n            id\\n            assetTagId\\n            assetClass {\\n                id\\n                name\\n                make\\n                model\\n            }\\n            serialNumber\\n        }\\n        location {\\n            locationId\\n            name\\n        }\\n        template {\\n            id\\n            title\\n            actualVersion {\\n                id\\n                name\\n                state\\n                rootTemplateId\\n            }\\n            versions {\\n                id\\n                name\\n                state\\n                rootTemplateId\\n                description\\n                createdAt\\n            }\\n        }\\n        jobsWithNotActualTemplateVersion {\\n            id\\n            template {\\n                id\\n                title\\n                actualVersion {\\n                    id\\n                    name\\n                    state\\n                    rootTemplateId\\n                }\\n            }\\n        }\\n        customEvidence {\\n            id\\n            name\\n            states\\n        }\\n        assignedUserDetails {\\n            id\\n            firstName\\n            lastName\\n            email\\n            isOnline\\n            avatarDetails {\\n                url\\n            }\\n        }\\n        contributors {\\n            id\\n            firstName\\n            lastName\\n            email\\n            isOnline\\n            avatarDetails {\\n                url\\n            }\\n        }\\n        notes {\\n            id\\n            step\\n            note {\\n                id\\n                text\\n                title\\n                type\\n                customEvidenceId\\n                meterEvidence\\n                meterEvidenceFault\\n                shapeNote {\\n                    mode\\n                }\\n                model {\\n                    id\\n                    name\\n                }\\n                files {\\n                    id\\n                    name\\n                    url\\n                }\\n                choiceNotes {\\n                    id\\n                    title\\n                    assetClass {\\n                        name\\n                    }\\n                    template {\\n                        id\\n                        title\\n                    }\\n                }\\n                meter {\\n                    id\\n                    name\\n                    unit {\\n                        name\\n                        valueType\\n                        description\\n                    }\\n                }\\n            }\\n        }\\n        steps {\\n            id\\n            resolveFault\\n            resolveDate\\n            completed\\n            startDate\\n            completionDate\\n            noteTypesOrder\\n            title\\n            step\\n            assignedUser\\n            requiredEvidence\\n            evidenceRequirements\\n            highlights {\\n                type\\n            }\\n            repairerDetails {\\n                id\\n                firstName\\n                lastName\\n                email\\n            }\\n            meterRequirements {\\n                value\\n                evaluationType\\n                meterId\\n                jobStepId\\n                noteId\\n            }\\n            notes {\\n                id\\n                text\\n                type\\n                title\\n                autoplay\\n                templateId\\n                actionType\\n                meter {\\n                    name\\n                }\\n                shapeNote {\\n                    mode\\n                }\\n                model {\\n                    id\\n                    name\\n                }\\n                files {\\n                    id\\n                    name\\n                    url\\n                }\\n                choiceNotes {\\n                    id\\n                    title\\n                    assetClass {\\n                        id\\n                        name\\n                    }\\n                    template {\\n                        id\\n                        title\\n                    }\\n                }\\n                model {\\n                    id\\n                    name\\n                }\\n                files {\\n                    name\\n                    fileType\\n                    url\\n                }\\n            }\\n        }\\n    }\\n}\\n\",\"variables\":{\"pageNumber\":1,\"itemsPerPage\":300000000,\"filters\":{\"locationId\":[],\"priority\":[],\"assetId\":[],\"faultFlag\":[],\"assetClass\":[],\"templates\":4,\"status\":[\"Assigned\",\"InProgress\",\"Unassigned\"],\"assignedUserId\":[]},\"sort\":{\"propertyName\":\"id\",\"reverse\":true},\"search\":{}}}"

    data, status_code = send_request(payload)
    all_jobs = data.get("data").get("jobsPage")
    print(len(all_jobs))
    for job in all_jobs:
        if job.get("id") == 28:
            print(job)
    return result


def add_durations_job_steep(job_step_id, durations):
    path = "rest/duration-plugin/add"

    payload = json.dumps({
        "table": "duration",
        "insert": [
            {
                "time": durations,
                "job_step_id": job_step_id
            }
        ],
        "returning": [
            "id",
            "job_step_id",
            "time"
        ]
    })

    response, status_code = send_request(payload, path)
    print(f"Saved time duration to job_id '{job_step_id}',  status_code={status_code}, response={response}")
    if status_code != 200:
        print(f"Error sending durations status_code={status_code}, response={response}")
        return [], status_code
    return {"complete": "success"}



