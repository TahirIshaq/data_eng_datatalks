import os

def download_from_url(urls):
    """
    Download file from URL
    urls(list): A list of URLs
    Return()
    """
    for url in urls:
        file_name = get_file_name_from_url(url)
        os.system(f"wget {url} -O {file_name}")
        return file_name


def get_file_name_from_url(url):
    """Returns file name from URL"""
    name_idx_st = len(url) - url[::-1].find("/")
    file_name = url[name_idx_st:]
    return file_name


def get_file_name_wo_ext(file_name):
    """Returns the file name without extension"""
    name_idx_end = file_name.find(".")
    file_name = file_name[:name_idx_end]
    return file_name

