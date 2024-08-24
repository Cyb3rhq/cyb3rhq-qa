import requests


OWNER = 'cyb3rhq'
CYB3RHQ_REPO = 'cyb3rhq'
CYB3RHQ_QA_REPO = 'cyb3rhq-qa'
GITHUB_API_URL = 'https://api.github.com'
HEADERS = {'Accept': 'application/vnd.github.v3+json'}
EXTRA_ARGS = '?per_page=100'


def _run_get_request(request_url, headers):
    response = requests.get(f"{GITHUB_API_URL}{request_url}", headers=headers)
    status_code = response.status_code

    if status_code != 200:
        raise ValueError(f"Could not run the GET request to {GITHUB_API_URL}/{request_url}. Status code {status_code}")

    all_data = response.json()

    while 'next' in response.links.keys():
        response = requests.get(response.links['next']['url'], headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Could not run the GET request to {GITHUB_API_URL}/{request_url}. Status "
                             f"code {response.status_code}")
        all_data.extend(response.json())

    return all_data


def _get_request_data(url, field_name):
    data = _run_get_request(url, HEADERS)

    return [item[field_name] for item in data]


def get_cyb3rhq_tags():
    return _get_request_data(f"/repos/{OWNER}/{CYB3RHQ_REPO}/tags{EXTRA_ARGS}", 'name')


def get_cyb3rhq_releases():
    return _get_request_data(f"/repos/{OWNER}/{CYB3RHQ_REPO}/releases{EXTRA_ARGS}", 'tag_name')


def get_cyb3rhq_master_version():
    response = requests.get('https://raw.githubusercontent.com/cyb3rhq/cyb3rhq/master/src/VERSION')

    return (response.text).split('\n')[0].replace('v', '')


def get_cyb3rhq_qa_master_version():
    response = requests.get('https://raw.githubusercontent.com/cyb3rhq/cyb3rhq-qa/master/version.json')

    return response.json()['version'].replace('v', '')


def version_is_released(version):
    releases = get_cyb3rhq_releases()
    v_version = f"v{version}" if not 'v' in version else version

    return v_version in releases


def branch_exist(branch_name, repository=CYB3RHQ_REPO):
    branches = get_branches(repository)

    return branch_name in branches


def get_branches(repository=CYB3RHQ_REPO):
    return _get_request_data(f"/repos/{OWNER}/{repository}/branches{EXTRA_ARGS}", 'name')


def get_last_cyb3rhq_version():
    return get_cyb3rhq_releases()[0]
