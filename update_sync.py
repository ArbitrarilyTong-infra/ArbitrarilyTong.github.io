import os
import json
import requests
from datetime import datetime


def send_get_request(url):
    """
    该函数向指定 URL 发送 GET 请求，如果请求成功，则返回 JSON 响应。
    
    :param url: `url` 参数是您想要向其发送 GET 请求的 API 端点的 URL。
    :return: 如果状态代码为 200，则为 JSON 响应。如果状态代码为 403，则打印一条有关超出速率限制的消息。如果请求期间出现错误，则会打印错误消息。
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("Rate limit exceeded. Please try again later or provide an access token for authentication.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during request: {e}")


def get_releases(repo_owner, repo_name):
    """
    函数“get_releases”接受存储库所有者和名称，构造 GitHub API 的 URL，并发送 GET 请求以检索指定存储库的版本。
    
    :param repo_owner: GitHub 上存储库的所有者。这通常是创建存储库的个人或组的用户名或组织名称。
    :param repo_name: GitHub 上存储库的名称。
    :return: 对 GitHub API 端点发出的 API 请求的响应，用于检索存储库的版本。
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    return send_get_request(url)


def get_release_files(release):
    """
    函数“get_release_files”检索给定版本的版本文件和版本主体。
    
    :param release: “release”参数是一个字典，其中包含有关发布的信息。它可能包括发布版本、发布日期以及与发布相关的资产列表等详细信息。
    :return: 两个值：对release_files_url 的 GET 请求的结果和发布的正文。
    """
    release_files_url = release['assets_url']
    return send_get_request(release_files_url), release['body']


def generate_release_info(file_info, name, tag, version, desc, mode_type):
    """
    函数“generate_release_info”接受各种参数并返回包含有关发布信息的字典。
    
    :param file_info: `file_info` 参数是一个字典，包含有关文件的信息。它应该具有以下键：
    :param name: name参数代表发布文件的文件名。
    :param tag: “tag”参数是一个字符串，表示文件的标签或版本名称。它用于标识文件的特定版本或发行版。
    :param version: “version”参数是一个字符串，表示版本的版本号。
    :param desc: “desc”参数是一个字符串，表示版本的描述。它提供有关该版本的附加信息或详细信息。
    :param mode_type: 参数“mode_type”用于指定释放的类型。它可以是表示发布类型的字符串，例如“stable”、“beta”、“alpha”等。
    :return: 包含有关发布的信息的字典。
    """
    return {
        "datetime": datetime.strptime(file_info["updated_at"], '%Y-%m-%dT%H:%M:%SZ').timestamp(),
        "filename": name,
        "id": file_info["id"],
        "tag": tag,
        "size": file_info["size"],
        "url": file_info['browser_download_url'],
        "version": version,
        "desc": desc,
        "type": mode_type
    }


def generate_release_list(release_files, release_name, mode_type, device_name, release_desc):
    """
    函数generate_release_list根据提供的发布文件、发布名称、模式类型、设备名称和发布描述生成发布信息列表。
    
    :param release_files: 包含有关发布文件信息的字典列表。每个字典都应该有一个“name”键，其中包含发布文件的名称。
    :param release_name: 发布的名称。
    :param mode_type: `mode_type` 参数是一个字符串，指定释放模式的类型。它可以有两个可能的值：“kernel”或“system”。
    :param device_name: “device_name”参数是为其生成发布列表的设备的名称。用于根据设备名称过滤发布文件。
    :param release_desc: `release_desc` 参数是一个字符串，表示版本的描述或详细信息。它提供有关该版本的其他信息，例如新功能、错误修复或任何其他相关信息。
    :return: 发布信息列表。
    """
    if release_files is None:
        return []

    release_list = []
    for file_info in release_files:
        if mode_type == "kernel":
            file_name = str(file_info["name"]).replace(".zip", "").split("_")[0]
            device, tag = file_name.split("-")
            if device == device_name:
                release_list.append(generate_release_info(file_info, file_name, tag, release_name, release_desc, mode_type))
        elif mode_type == "system":
            file_name = str(file_info["name"]).replace(".zip", "").split("-")
            name = "-".join(file_name[:2])
            tag = file_name[3]
            if file_name[4] == device_name:
                release_list.append(generate_release_info(file_info, name, tag, file_name[2] + "@" + release_name, release_desc, mode_type))
    return release_list


def get_repo_release_info(repo_owner, repo_name, mode_type, device_name):
    """
    函数“get_repo_release_info”检索给定存储库、模式类型和设备名称的发布信息。
    
    :param repo_owner: 存储库的所有者（例如 GitHub 上的用户名或组织名称）。
    :param repo_name: `repo_name` 参数是存储库的名称。它是一个字符串，指定要从中获取发布信息的存储库的名称。
    :param mode_type: `mode_type` 参数用于指定发布的模式。它可以是特定版本，例如“稳定”或“测试版”，也可以是该版本重点关注的特定特性或功能。
    :param device_name: `device_name` 参数是您要检索其版本信息的设备的名称。
    :return: 给定存储库、模式类型和设备名称的发布信息列表。
    """
    releases = get_releases(repo_owner, repo_name)
    release_list = []

    if releases is not None:
        for release in releases:
            release_name = release['name']
            release_files, release_desc = get_release_files(release)
            release_list.extend(generate_release_list(release_files, release_name, mode_type, device_name, release_desc))

    return release_list


def generate_save_path(device_name):
    """
    该函数根据当前工作目录和设备名称生成 JSON 文件的保存路径。
    
    :param device_name: device_name 参数是一个字符串，表示要为其生成保存路径的设备的名称。
    :return: 基于设备名称的 JSON 文件的保存路径。
    """
    root_dir = os.getcwd()
    save_path = os.path.join(root_dir, device_name + ".json")
    return save_path



# `if __name__ == '__main__':` 块是一种常见的 Python 习惯用法，它允许脚本作为独立程序执行或作为模块导入。
if __name__ == '__main__':
    with open('sync.json') as f:
        sync_list = json.load(f)
        for device, repo_list in sync_list.items():
            release_list = []
            if kernel_repo := repo_list.get("kernel_repo"):
                owner, repo = kernel_repo.split('/')
                release_list.extend(get_repo_release_info(owner, repo, "kernel", device))
            if system_repo := repo_list.get("system_repo"):
                owner, repo = system_repo.split('/')
                release_list.extend(get_repo_release_info(owner, repo, "system", device))
            save_path = generate_save_path(device)
            with open(save_path, "w", encoding='utf-8') as f:
                json.dump(release_list, f, indent=2, sort_keys=True, ensure_ascii=False)
