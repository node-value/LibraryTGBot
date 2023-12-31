import os
from pydrive2.drive import GoogleDrive
from pydrive2.auth  import GoogleAuth


class GoogleDriveService:
    temp_storage_folder = 'temp_file_storage'
    
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        self.section   = dict()
        self.title     = dict()
        self.keyboards = dict()
        self.create_dict_of_section_title_and_keyboards()
    
    def create_dict_of_section_title_and_keyboards(self, folder_id=None):
        if folder_id == None: folder_id = Constants.ROOT_FOLDER_ID
        item_list = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
        self.keyboards[folder_id] = item_list
        for item in item_list:
            if item['mimeType'] != 'application/vnd.google-apps.folder':
                self.title[item['title']] = item['id']
            else:
                self.section[item['title']] = item['id']
                self.create_dict_of_section_title_and_keyboards(item["id"])
    
    def is_section(self, name):
        return name in self.section
    
    def get_list_of_content_in_section(self, section_name):
        section_id = self.section[section_name]
        item_list = self.keyboards[section_id]
        return [ section["title"] for section in item_list ]
    
    def get_document(self, document_name):
        downloaded_file = self.drive.CreateFile({'id': self.title[document_name]})
        path = os.path.join(os.getcwd(), GoogleDriveService.temp_storage_folder, document_name)
        downloaded_file.GetContentFile(path)
        return path
 
    def get_list_of_root_sections(self):    
        item_list = self.drive.ListFile({'q': f"'{Constants.ROOT_FOLDER_ID}' in parents and trashed=false"}).GetList()
        return [ section["title"] for section in item_list ]


