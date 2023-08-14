import os
import sys
import random
import subprocess
import glob
import asyncio
import pdb
import re
import pandas as pd
from typing import Dict
from typing import List
from typing import Generator
from typing import Any

def _target_generator(root_path: str) -> Generator[str, None, None]:
    """
    generator monitor files
    :param root_path: folder path which you want to monitor
    """
    get_username = lambda root_path: re.search("(?P<username>\d{8}[a-z]{3})", root_path).groupdict()
    for path in glob.glob(root_path):
        account = get_username(path)['username']
        for dir_path, dir_names, file_names in os.walk(path):
            for file_name in file_names:
                filepath = os.path.join(dir_path, file_name)
                yield account, filepath

async def get_filesize(username: str, path: str) -> Dict[str, str]:
    """
    Measure the size of a specific file.
    :param username: folder user account name
    :param path: file path

    :return output: data info (username, filepath, filesize)
    """
    filesize = os.path.getsize(path)
    output = {
        "username": username,
        "filepath": path,
        "filesize": filesize
    }
    return output

async def get_all_filesize(root_path: str) -> pd.DataFrame:
    """
    Organize the data into a dataframe
    :param root_path: folder path which you want to monitor
    :return data: dataframe with columns: username, filepath, filesize
    """

    tasks = [get_filesize(username, path) for username, path in _target_generator(root_path)]

    tmp = list()
    for task in asyncio.as_completed(tasks):
        output = await task
        tmp.append(output)

    data = pd.DataFrame(tmp)

    return data

async def analysis_user_usage(data: pd.DataFrame, key: str, info: Dict[str, str]) -> Dict[str, Any]:
    """
    :param data: dataframe with columns: username, filepath, filesize
    :param key: column to analysis
    :param info: information of group
    """
    result = data[key].sum()
    output = {**info, **{"foldersize":result}}
    return output

async def python_du(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Analysis all user folder size
    :param dataset: dataframe with columns: username, filepath, filesize
    :return data: dataframe with columns: username, foldersize
    """

    group_cols = ['username']
    tasks, task_result = list(), list()

    def _get_info(group_cols, groups):
        if not isinstance(groups, tuple):
            groups = [groups]
        return dict(zip(group_cols, groups))

    pack_task = lambda dataset, group_cols, group: analysis_user_usage(
        data, "filesize",
        _get_info(group_cols, groups)
    )

    for groups, data in dataset.groupby(group_cols):
        tasks.append(
            pack_task(dataset, group_cols, groups)
        )

    for task in asyncio.as_completed(tasks):
        output = await task
        task_result.append(output)

    data = pd.DataFrame(task_result)
    return data

