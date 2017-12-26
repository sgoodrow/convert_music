import os
import ffmpy

class Main:
    ROOT = '/mnt/c/Picard_DeleteAfter2017/test'
    CONVERTED_EXT = '.mp3'
    CANNOT_CONVERT_EXT = '.m4p'
    num_files = 0
    num_folders = 0
    num_mp3s = 0
    num_converted = 0
    num_failed = 0
    num_m4ps_removed = 0
    num_m4ps_skipped = 0

    def main(self):
        self.handle_folder(self.ROOT)
        print('num_files %d' % self.num_files)
        print('num_folders %d' % self.num_folders)
        print('num_mp3s %d' % self.num_mp3s)
        print('num_converted %d' % self.num_converted)
        print('num_failed %d' % self.num_failed)
        print('num_m4ps_removed %d' % self.num_m4ps_removed)
        print('num_m4ps_skipped %d' % self.num_m4ps_skipped)

    def handle_folder(self, folder_path):
        self.num_folders = self.num_folders + 1
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isdir(full_path):
                self.handle_folder(full_path)
            else:
                self.handle_file(file_name, full_path, folder_path)

    def handle_file(self, file_name, full_path, folder_path):
        self.num_files = self.num_files + 1
        if self.need_convert(file_name, folder_path):
            self.convert(full_path)

    def need_convert(self, file_name, folder_path):
        root, ext = os.path.splitext(file_name)
        if ext.lower() == self.CONVERTED_EXT:
            self.num_mp3s = self.num_mp3s + 1
            return False
        else:
            full_destination_path = os.path.join(folder_path, root + self.CONVERTED_EXT)

            # catch m4ps and delete them if there is an mp3 already
            # not: m4ps cannot be converted and have DRM
            dest_exists = os.path.exists(full_destination_path)            
            if ext.lower() == self.CANNOT_CONVERT_EXT:
                if dest_exists:
                    os.remove(os.path.join(folder_path, file_name))
                    self.num_m4ps_removed = self.num_m4ps_removed + 1
                else:
                    self.num_m4ps_skipped = self.num_m4ps_skipped + 1
                return False

            return not dest_exists

    def convert(self, full_path):
        root, ext = os.path.splitext(full_path)
        new_full_path = root + self.CONVERTED_EXT
        try:
            ff = ffmpy.FFmpeg(inputs={full_path: None}, outputs={new_full_path: ['-ab', '160k']})
            ff.run()
            self.num_converted = self.num_converted + 1
        except:
            print('failed to convert %s' % full_path)
            try:
                os.remove(new_full_path)
                self.num_failed = self.num_failed + 1
            except:
                print('failed to delete artifact %s' % new_full_path)

if __name__ == "__main__":
    # execute only if run as a script
    Main().main()