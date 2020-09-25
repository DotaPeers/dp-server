
def getProfilePicturePath(accountId: int):
    """
    Used to split filenames into subdirectories to prevent having one directory with too many files.
    """

    id_str = str(accountId)
    a = id_str[0]
    b = id_str[1]

    return f'{a}/{b}/{accountId}.png'
