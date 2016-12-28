import os

'''
返回根路径
根路径为：Alex_DM 文件夹

如果根路径有变化，请更改default_root变量的值
'''


def root():
    """
    Finds the root of the project and return it as string.

    The root is the directory named Alex_DM.

    """

    default_root = "Alex_DM"

    path, directory = os.path.split(os.path.abspath(__file__))

    while directory and directory != default_root:
        path, directory = os.path.split(path)

    if directory == default_root:
        return os.path.join(path, directory)
    else:
        raise Exception("Couldn't determine path to the project root.")


if __name__ == '__main__':
    root()
