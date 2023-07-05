import json
import os
from datetime import datetime

import requests
import sys


def check_and_return(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            releases = response.json()
            return releases
        elif response.status_code == 403:
            print(
                "Rate limit exceeded. Please try again later or provide an access token for authentication.")
            return None
        else:
            print(f"Error occurred during request: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during request: {e}")
        return None


def get_releases(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    return check_and_return(url)


def get_release_files(release):
    release_files_url = release['assets_url']
    return check_and_return(release_files_url)


def generate_release_dict(release_files, release_name, mode_type):
    if release_files is None:
        return

    release_infos = []
    for file_info in release_files:
        release_info = generate_kernel_release_dict(file_info,
                                                    release_name) if mode_type == "kernel" else generate_system_release_dict(
            file_info, mode_type)
        release_infos.append(release_info)
    return release_infos


def generate_kernel_release_dict(file_info, release_name):
    name = str(file_info["name"])
    tag = "KernelSU" if "kernelsu" in name else "Original"
    return {
        "datetime": str(datetime.strptime(file_info["updated_at"], '%Y-%m-%dT%H:%M:%SZ')),
        "filename": name,
        "id": file_info["id"],
        "tag": tag,
        "size": file_info["size"],
        "url": file_info['browser_download_url'],
        "version": release_name
    }


# TODO
def generate_system_release_dict(file_info, release_name):
    return {
        "datetime": str(datetime.strptime(file_info["updated_at"], '%Y-%m-%dT%H:%M:%SZ')),
        "filename": file_info["name"],
        "id": file_info["id"],
        "tag": "Tong",
        "size": file_info["size"],
        "url": file_info['browser_download_url'],
        "version": release_name
    }


def get_repo_release_info(repo_owner, repo_name, mode_type):
    releases = get_releases(repo_owner, repo_name)

    download_list = []

    if releases is not None:
        for release in releases:
            release_name = release['name']
            release_files = get_release_files(release)
            download_list.append(generate_release_dict(release_files, release_name, mode_type))

    return download_list


def generate_save_path(mode_type, device_name):
    root_dir = os.getcwd()
    combine_path = os.path.join(root_dir, mode_type, device_name)
    os.makedirs(combine_path, exist_ok=True)  # mkdir -p
    combine_path = os.path.join(combine_path, mode_type + ".json")
    return combine_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the repository author and name as command line arguments.")
    else:

        repo_arg = sys.argv[1]  # template: <owner or org>/<repo name>
        mode = sys.argv[2]  # option: kernel, system
        device = sys.argv[3]  # option: kernel, system

        owner, repo = repo_arg.split('/')

        save_path = generate_save_path(mode, device)

        download_list = get_repo_release_info(owner, repo, mode)
        with open(save_path, "w", encoding='utf-8') as f:
            json.dump(download_list, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
