import os
def getFilesInDir(directory,*identyfier:str):
    filepaths = []

    filenames = os.listdir(directory)

    for filename in filenames:
        if identyfier == None:
            filepaths.append(os.path.join(directory, filename))
        else:
            if filename.endswith(identyfier):
                filepaths.append(os.path.join(directory,filename))
    return filepaths


