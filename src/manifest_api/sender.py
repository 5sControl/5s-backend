import re

from src.manifest_api.get_data import send_request
from src.manifest_api.models import ManifestConnection
from src.CameraAlgorithms.models import ZoneCameras


def send_manifest_response(data):
    manifest_connection = ManifestConnection.objects.last()

    asset_class_id = manifest_connection.asset_class_id
    asset_id = manifest_connection.asset_id
    location_id = manifest_connection.location_id
    job_template = manifest_connection.job_template
    assigned_user = manifest_connection.assigned_user

    job_id = create_job(location_id, assigned_user, job_template, asset_id)

    if not job_id:
        return print(f'Could not create job status code {job_id.status_code}')

    zone_ids = [entry['zone_id'] for entry in data]

    for zone_id in set(zone_ids):
        workplace = ZoneCameras.objects.get(id=zone_id).workplace
        match = re.search(r'Step (\d+)', workplace)
        step = int(match.group(1))

        start_job_step(job_id, step)
        print("start_job_step job step", step)
        complete_job_step(job_id, step)
        print("complete_job_step job step", step)

    print("Sending all jobs to manifest")


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
