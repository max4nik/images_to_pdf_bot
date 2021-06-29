import os


class Helper:
    @staticmethod
    def delete_files_in_folder(folder):
        filelist = [file for file in os.listdir(folder)]
        for file in filelist:
            os.remove(os.path.join(folder, file))
