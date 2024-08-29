import json
import logging
import re
from datetime import datetime, timedelta

from celery import shared_task

from src.OrderView.utils import get_package_video_info, get_skany_video_info
from src.manifest_api.get_data import send_request, upload_file, get_steps_by_asset_class
from src.manifest_api.service import sorted_response, get_jobs_manifest

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
    if not sorted_data:
        return
    for item in sorted_data:
        print("item", item)
        name_workplace = item.get('name_workplace')
        ip_camera = item['steps'][0]['all_images_zones'][0].split('/')[1]
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
        list_ids_job_steps = get_id_job_steps(job_id)
        for step_data in item.get('steps'):
            print("step_data", step_data)
            step = step_data.get('step')
            all_images = step_data.get('all_images_zones', [])
            durations = step_data.get('all_durations')
            start_time = step_data.get('start_time')

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

            add_durations_job_steep(list_ids_job_steps[step - 1], durations, start_time, ip_camera)
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


def get_id_job_steps(job_id):
    payload = "{\"query\":\"query($id: Int!) {\\n    job(id: $id) {\\n        id\\n        parentJobId\\n        assetId\\n        autoplay\\n        locationId\\n        elapsedTime\\n        completedStepPercent\\n        title\\n        description\\n        priority\\n        externalId\\n        templateId\\n        jobType\\n        creationDate\\n        startDate\\n        completionDate\\n        status\\n        assignedUser\\n        associatedGroupChatId\\n        teamSetupCompleted\\n        workItemType\\n        hasOpenFaults\\n        newJobPromptCancelled\\n        faults {\\n            id\\n            resolvedAt\\n            description\\n            createdByUserId\\n            jobStepId\\n        }\\n        asset {\\n            id\\n            assetTagId\\n            assetClass {\\n                id\\n                name\\n                make\\n                model\\n            }\\n            serialNumber\\n        }\\n        location {\\n            locationId\\n            name\\n        }\\n        template {\\n            id\\n            title\\n            actualVersion {\\n                id\\n                name\\n                state\\n                rootTemplateId\\n            }\\n            versions {\\n                id\\n                name\\n                state\\n                rootTemplateId\\n                description\\n                createdAt\\n            }\\n        }\\n        jobsWithNotActualTemplateVersion {\\n            id\\n            template {\\n                id\\n                title\\n                actualVersion {\\n                    id\\n                    name\\n                    state\\n                    rootTemplateId\\n                }\\n            }\\n        }\\n        customEvidence {\\n            id\\n            name\\n            states\\n        }\\n        assignedUserDetails {\\n            id\\n            firstName\\n            lastName\\n            email\\n            isOnline\\n            avatarDetails {\\n                url\\n            }\\n        }\\n        contributors {\\n            id\\n            firstName\\n            lastName\\n            email\\n            isOnline\\n            avatarDetails {\\n                url\\n            }\\n        }\\n        notes {\\n            id\\n            step\\n            note {\\n                id\\n                text\\n                title\\n                type\\n                customEvidenceId\\n                meterEvidence\\n                meterEvidenceFault\\n                shapeNote {\\n                    mode\\n                }\\n                model {\\n                    id\\n                    name\\n                }\\n                files {\\n                    id\\n                    name\\n                    url\\n                }\\n                choiceNotes {\\n                    id\\n                    title\\n                    assetClass {\\n                        name\\n                    }\\n                    template {\\n                        id\\n                        title\\n                    }\\n                }\\n                meter {\\n                    id\\n                    name\\n                    unit {\\n                        name\\n                        valueType\\n                        description\\n                    }\\n                }\\n            }\\n        }\\n        steps {\\n            id\\n            resolveFault\\n            resolveDate\\n            completed\\n            startDate\\n            completionDate\\n            noteTypesOrder\\n            title\\n            step\\n            assignedUser\\n            requiredEvidence\\n            evidenceRequirements\\n            highlights {\\n                type\\n            }\\n            repairerDetails {\\n                id\\n                firstName\\n                lastName\\n                email\\n            }\\n            meterRequirements {\\n                value\\n                evaluationType\\n                meterId\\n                jobStepId\\n                noteId\\n            }\\n            notes {\\n                id\\n                text\\n                type\\n                title\\n                autoplay\\n                templateId\\n                actionType\\n                meter {\\n                    name\\n                }\\n                shapeNote {\\n                    mode\\n                }\\n                model {\\n                    id\\n                    name\\n                }\\n                files {\\n                    id\\n                    name\\n                    url\\n                }\\n                choiceNotes {\\n                    id\\n                    title\\n                    assetClass {\\n                        id\\n                        name\\n                    }\\n                    template {\\n                        id\\n                        title\\n                    }\\n                }\\n                model {\\n                    id\\n                    name\\n                }\\n                files {\\n                    name\\n                    fileType\\n                    url\\n                }\\n            }\\n        }\\n    }\\n}\\n\",\"variables\":{\"id\":"+f"{job_id}"+"}}"
    response, status_code = send_request(payload)
    data = response.get('data').get('job').get('steps')
    ids = [item['id'] for item in data]
    return ids


def get_all_works_manifest(from_date_str, to_date_str, type_operations="operations"):
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(milliseconds=1)

    from_date_ms = int(from_date.timestamp() * 1000)
    to_date_ms = int(to_date.timestamp() * 1000)


    path = "rest/duration-plugin/get"

    payload = json.dumps({
        "table": "duration",
        "conditions": {
            "duration.start_time": {
                "OP": "BETWEEN",
                "value": [from_date_ms, to_date_ms]
            }
        },
        "joins": [
            {
                "table": "job_step",
                "first": "job_step.id",
                "second": "duration.job_step_id",
                "type": "left"
            },
            {
                "table": "jobs",
                "first": "jobs.id",
                "second": "job_step.job_id",
                "type": "left"
            },
            {
                "table": "assets",
                "first": "assets.id",
                "second": "jobs.asset_id",
                "type": "left"
            },
            {
                "table": "templates",
                "first": "templates.id",
                "second": "jobs.template_id",
                "type": "left"
            }
        ],
        "orderBy": {
            "duration.id": "asc"
        }
    })

    data, status_code = send_request(payload, path)
    result = get_jobs_manifest(data, type_operations)
    return result


def add_durations_job_steep(job_step_id, durations, start_time, ip_camera):
    print("start_time", start_time)
    path = "rest/duration-plugin/add"
    dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
    obj_start_time = int(dt.timestamp() * 1000)
    print("obj_start_time", obj_start_time)
    payload = json.dumps({
        "table": "duration",
        "insert": [
            {
                "start_time": obj_start_time,
                "time": durations,
                "job_step_id": job_step_id,
                "ip_camera": ip_camera
            }
        ],
        "returning": [
            "id",
            "job_step_id",
            "time"
        ]
    })

    response, status_code = send_request(payload, path)
    print(f"Saved time duration to job_id '{job_step_id}', "
          f"start_time={start_time}, status_code={status_code}, response={response}")
    if status_code != 200:
        print(f"Error sending durations status_code={status_code}, response={response}")
        return [], status_code
    return {"complete": "success"}


def get_operation_by_details_manifest(operation_id):
    path = "rest/duration-plugin/get"

    payload = json.dumps({
        "table": "duration",
        "conditions": {
            "job_step.id": f"{operation_id}"
        },
        "joins": [
            {
                "table": "job_step",
                "first": "job_step.id",
                "second": "duration.job_step_id",
                "type": "left"
            }
        ],
        "orderBy": {
            "duration.id": "asc"
        },
        "limit": 3
    })
    response, status_code = send_request(payload, path)
    data = response[0]
    time = int(data.get("start_time"))
    print(f"find_time: {convert_milliseconds(time)}")
    ip_camera = data.get("ip_camera")
    if not ip_camera:
        ip_camera = "192.168.1.164"
    result = {
        "id": data.get("id"),
        "orId": data.get("job_step_id"),
        "oprName": data.get("job_step")[0].get("title"),
        # "elType": elementType,
        "sTime": int(data.get("start_time")),
        "eTime": int(data.get("start_time")) + int(data.get("time") * 1000),
        # "frsName": firstName,
        # "lstName": lastName,
        "status": data.get("job_step")[0].get("completed"),
        "video": get_skany_video_info(time, ip_camera),
    }

    if status_code != 200:
        print(f"Error sending durations status_code={status_code}, response={response}")
        return [], status_code
    return result


def convert_milliseconds(ms):
    dt = datetime.utcfromtimestamp(ms / 1000.0)
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
