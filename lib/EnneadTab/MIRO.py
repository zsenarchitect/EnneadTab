import traceback
import os
import datetime
import json

def log_error(error):
    error += "\n\n######If you have EnneadTab UI window open, just close the window. Do no more action, otherwise the program might crash.##########\n#########Not sure what to do? Msg Sen Zhang, you have dicovered a important bug and we need to fix it ASAP!!!!!########"
    error_file = "{}\Documents\EnneadTab Settings\Local Copy Dump\error_log.txt".format(os.environ["USERPROFILE"])

    with open(error_file, "w") as f:
        f.write(error)


try:
    from PIL import Image
    import requests
except:
    error = traceback.format_exc()
    log_error(error)

##############################################################
HOSTER_FOLDER = "L:\\4b_Applied Computing"
MISC_FOLDER = "{}\\01_Revit\\04_Tools\\08_EA Extensions\\Project Settings\\Misc".format(HOSTER_FOLDER)
def get_api_key(key_name):
    
    file_path = r"{}\EA_API_KEY.json".format(MISC_FOLDER)

    data = read_json_as_dict(file_path)
    return data.get(key_name, None)



def read_json_as_dict(filepath, use_encode=False, create_if_not_exist = False):
    """get the data saved in json as dict

    Args:
        filepath (_type_): _description_
        use_encode (bool, optional): for Chinese char file it might need encoding. Defaults to False.

    Returns:
        dict | None: _description_
    """
    
    with open(filepath, encoding='utf8') as f:
        data = json.load(f)
    return data

def read_json_as_dict_in_dump_folder(file_name, use_encode=False, create_if_not_exist=False):
    """direct access the json file from dump folder

    Args:
        file_name (_type_): _description_
        use_encode (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    filepath = get_EA_dump_folder_file(file_name)
    return read_json_as_dict(filepath, use_encode, create_if_not_exist)


def get_EA_dump_folder_file(file_name):
    """include extension"""
    return "{}\Documents\EnneadTab Settings\Local Copy Dump\{}".format( os.environ["USERPROFILE"], file_name)

def get_formatted_current_time():
    """-->2023-05-16_11-33-55"""
    now = datetime.datetime.now()
    return get_formatted_time(now)


def get_formatted_time(input_time):
    #  if input is float, convert to datetime object first:
    if isinstance(input_time, float):
        input_time = datetime.datetime.fromtimestamp(input_time)
    
    year, month, day = '{:02d}'.format(input_time.year), '{:02d}'.format(input_time.month), '{:02d}'.format(input_time.day)
    hour, minute, second = '{:02d}'.format(input_time.hour), '{:02d}'.format(input_time.minute), '{:02d}'.format(input_time.second)
    return "{}-{}-{}_{}-{}-{}".format(year, month, day, hour, minute, second)
###############################################################################
def get_token():
    return get_api_key("miro_oauth")


class Miro:
    def __init__(self, board_id):
        self.board_id = board_id
        self.token = get_token()


    @staticmethod
    def get_all_boards_info(keyword = None):
        url = "https://api.miro.com/v2/boards"
        if keyword:
            url = url + "?query={}".format(keyword)

        headers = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(get_token())
        }

        response = requests.get(url, headers=headers)


        # print(response.text)
        return response.json()
        
    @staticmethod
    def create_board(board_name,
                    description = ""):
        
        url = "https://api.miro.com/v2/boards"

        payload = {
            "name": board_name,
            "description": description
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer {}".format(get_token())
        }

        response = requests.post(url, json=payload, headers=headers)

        return Miro(response.json()["id"])



    @staticmethod
    def get_board(board_id_or_url):

        if "board/" in board_id_or_url:
            board_id_or_url = board_id_or_url.split("board/")[-1].replace("/", "")

        return Miro(board_id_or_url)




    def create_frame(self,
                     frame_data,
                     position,
                     geometry):
        pass

    def update_frame(self,
                     frame_id,
                     frame_data,
                     position = None,
                     geometry = None):
        pass
        # should also rename the frame with update timestamp

    def get_frame_by_name(self, frame_name):
        return self.find(frame_name, "frame")



    
    def get_frame_children(self,
                           frame_or_frame_id):
        if frame_or_frame_id.haskey("id"):
            frame_id = frame_or_frame_id['id']
        else:
            frame_id = frame_or_frame_id
        


        url = "https://api.miro.com/v2/boards/{}/items?parent_item_id={}".format(self.board_id,
                                                                                 frame_id)

        headers = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers=headers)

 
        return response.json()



    def create_images(self, creation_datas):
        url = "https://api.miro.com/v2/boards/{}/images".format(self.board_id)

        
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        files = []
        for creation_data in creation_datas:
            image_full_path = creation_data["full_path"]
            position = creation_data["position"]
            width = creation_data["width"]
            title = creation_data["title"]
            
            file = (
                "resource",
                (os.path.basename(image_full_path), open(image_full_path, "rb"), "image/jpg"),
            ),
            (
                "data",
                (
                    None,
                    json.dumps(
                        {
                            "title": title,
                            "position": {
                                "x": position[0],
                                "y": position[1],
                            },
                            "geometry": {
                                "width": width,
                                "rotation": 0,
                            }
                        }
                    ),
                    "application/json",
                ),
            )

            files.append(file)
        
        response = requests.post(url, headers=headers, data={}, files=files)
        print (response.text)
    
    def create_image(self,
                     image_full_path,
                     position,
                     width = None,
                     image_title = None, 
                     parent = None):

        url = "https://api.miro.com/v2/boards/{}/images".format(self.board_id)


        title = image_title if image_title else image_full_path.split("/")[-1]

        creation_data ={
                    "title": title,
                    "position": {
                                "x": position[0],
                                "y": position[1]
                    }
                }
        if width:
            creation_data.update({"geometry": {"width": width}})

        if parent:
            creation_data.update({"parent": {"id": parent}})
        files = [
            (
                "resource",
                (os.path.basename(image_full_path), open(image_full_path, "rb"), "image/jpg"),
            ),
            (
                "data",
                (
                    None,
                    json.dumps(
                        creation_data
                    ),
                    "application/json",
                ),
            ),
        ]

        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }

        response = requests.post(url, headers=headers, data={}, files=files)
        # print (response.text)

        return response.json()

        

    def update_image(self,
                     image_id,
                     image_full_path,
                     image_title = None,
                     position = None,
                     width = None,
                     parent = None):
        
        url = "https://api.miro.com/v2/boards/{}/images/{}".format(self.board_id,
                                                                   image_id)


        title = image_title if image_title else image_full_path.split("/")[-1]
        

        creation_data ={
                            "title": title,
        }

        if position:
            creation_data.update({"position": {"x": position[0], "y": position[1]}})

        if width:
            creation_data.update({"geometry": {"width": width}})

        if parent:
            creation_data.update({"parent": {"id": parent}})


        files = [
            (
                "resource",
                (os.path.basename(image_full_path), open(image_full_path, "rb"), "image/jpg"),
            ),
            (
                "data",
                (
                    None,
                    json.dumps(
                        creation_data
                    ),
                    "application/json",
                ),
            ),
        ]

        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }

        response = requests.patch(url, headers=headers, data={}, files=files)
        # print (response.text)

        return response.json()

    def create_star(self,
                    position,
                    width,
                    text = "",
                    color = "#ffa500"):

        url = "https://api.miro.com/v2/boards/{}/shapes".format(self.board_id)

        payload = {
            "data": {
                "shape": "star"
            },
            "style": { "fillColor": color ,
                      "fillOpacity" : "1.0"},
            "position": {
                "x": position[0],
                "y": position[1]
            },
            "geometry": { "width": width,
                         "height": width}
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer {}".format(self.token)
        }

        response = requests.post(url, json=payload, headers=headers)
        print("create a star")
        # print(response.text)


        
    def create_sticky_note(self,
                           sticky_note_data,
                           position,
                           geometry,
                           parent = None):
        pass


    def create_connection(self,
                          start_id,
                          end_id,
                          connection_text = None):

        url = "https://api.miro.com/v2/boards/{}/connectors".format(self.board_id)

        payload = {
            "startItem": {
                "id": start_id,
                "snapTo": "auto"
            },
            "endItem": {
                "id": end_id,
                "snapTo": "auto"
            }
        }

        if connection_text:
            payload.update({"captions": [{ "content": connection_text }]})
            
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer {}".format(self.token)
        }

        response = requests.post(url, json=payload, headers=headers)

        # print(response.text)

        return response.json()["id"]


    def highlight_frames(self, frame_ids):
        if not isinstance(frame_ids, list):
            frame_ids = [frame_ids]


        for frame_id in frame_ids:
            pass



    def purge_stars(self):
        url = "https://api.miro.com/v2/boards/{}/items?limit=50&type=shape".format(self.board_id)

        headers = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers=headers)
        print (response.text)

 

        if response.json()["size"]==0:
            print ("there is nothing on the board")
            return None
        
        star_ids = []
        for item in response.json()["data"]:

            if item["data"]["shape"] == "star":
                star_ids.append(item["id"])


        for id in star_ids:
            print ("delete a star")
            

            url = "https://api.miro.com/v2/boards/{}/shapes/{}".format(self.board_id, id)

            headers = {
                "accept": "application/json",
                "authorization": "Bearer {}".format(self.token)
            }

            response = requests.delete(url, headers=headers)
           
            print (response.text)

                


    def find(self,
             human_name,
             type = None):
        """_summary_

        Args:
            human_name (single): _description_
            type (_type_, optional): _description_. Defaults to None.

        Returns:
            single item, depeden on the input type of human names
        """
 
        print ("searching for {}".format(human_name))
        
        url = "https://api.miro.com/v2/boards/{}/items".format(self.board_id)

        headers = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(self.token)
        }

        response = requests.get(url, headers=headers)

        # print (response.text)


        if response.json()["size"]==0:
            print ("there is nothing on the board")
            return None
        

        for item in response.json()["data"]:
            if type:
                if item["type"] != type:
                    continue

            if human_name in item["data"]["title"]:
                print ("found {}".format(item["data"]["title"]))
                return item

        return None

##################################################################

def update_revit_sheets_on_miro(sheet_imgs, miro_board_url):
    """_summary_

    Args:
        sheet_imgs (list): a typical img fiel name looks like this folder\\{guid}^{sheetNum}^{sheetName}.jpg
        miro_board_url (_type_): _description_

    Returns:
        _type_: _description_
    """
    miro_board = Miro.get_board(miro_board_url)

    miro_board.purge_stars()


    for i, sheet_img in enumerate(sheet_imgs):
        print ("\n\n### Processs {} of {} sheets".format(i+1, len(sheet_imgs)))
        guid = sheet_img.split("\\")[-1].split("^")[0]
        full_path = sheet_img
        sheet_num = sheet_img.split("\\")[-1].split("^")[1]
        sheet_name = sheet_img.split("\\")[-1].split("^")[2].split(".")[0]
 

        image_title = "[{}]_[{}]_{}".format(sheet_num, sheet_name, guid)
        image = miro_board.find(guid, "image")


        if not image or len(image) == 0:
            print("creating image {}".format(image_title))

            img = Image.open(full_path)
            width, height = img.size

            image = miro_board.create_image(full_path,
                                            (i*(width *1.2),0),
                                            image_title=image_title)
        else:
            # print (image)
            image_id = image["id"]
            print("updating image {}".format(image_title))
            image_title = image_title + "[Uploaded at {}]".format(get_formatted_current_time())
            image = miro_board.update_image(image_id, 
                                            full_path,
                                            image_title=image_title)


        x, y = image["position"]["x"], image["position"]["y"]
        w, h = image["geometry"]["width"], image["geometry"]["height"]
        miro_board.create_star((x + w*0.5, y - h*0.5),
                               image["geometry"]["width"]*0.15)

    print("!!!!!!!!!!!!!! Finish updating miro")

    return miro_board

def main():
    data = read_json_as_dict_in_dump_folder("miro.json")
    app, url, sheet_imgs = data["app"], data["url"], data["images"]

    if app == "revit_sheet":
        update_revit_sheets_on_miro(sheet_imgs, url)



    
if __name__ == "__main__":
    try:
        main()
    except:
        error = traceback.format_exc()
        log_error(error)
        
    # board = Miro.create_board("test")
    # info = Miro.get_all_boards_info("DumpSheet")
    # # info = Miro.get_all_boards_info()

    #print (info)
    # test_board_id = info["data"][0]["id"]
    # print(test_board_id)


    # board = Miro.get_board(test_board_id)
    # print (board)