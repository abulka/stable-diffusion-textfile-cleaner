from time import sleep
import os
import shutil
import random
import flet
from flet import ListView, Page, Text, TextField, FilledTonalButton, FilledButton, ElevatedButton, icons, colors, Row, ButtonStyle
from flet import FilePicker, FilePickerResultEvent, padding, Container, ProgressRing, Column
from flet import Page, KeyboardEvent, Dropdown, dropdown, Image
from main import list_files, list_png, create_two_sets, find_missing_files, add_dir_root_and_txt_extension
import preferences, choose_favourites
from preferences import edit_preferences, model_add_favourite_path, model_get_last_favourite_dir, model_get_last_favourites
from choose_favourites import choose_favourite
import settings
from settings import model_get_initial_directory
# import smokesignal

# these should probably be in the model
bad_txt_files = []
chosen_path = None  # user will override later
img = None

def main(page: Page):
    settings.page = page

    global chosen_path
    global img

    page.title = "stable diffusion textfile cleaner"
    page.window_width = 1200
    page.window_center()

    # @smokesignal.on('chose_dir')
    # def listener_chose_dir(arg):
    def listener_chose_dir(topic, arg):
        print('listener_chose_dir', arg)
        chosen_path = arg['path']
        txt1.value = chosen_path
        txt1.update()
        model_add_favourite_path(chosen_path)
        print('chosen_path AFTER dir selection', chosen_path)
        button_scan_clicked(None)

    page.pubsub.subscribe_topic("chose_dir", listener_chose_dir)

    def on_dialog_result(e: FilePickerResultEvent):
        global chosen_path
        print("Selected files:", e.files)
        print("Selected file or directory:", e.path)
        if e.path is None:
            print("User cancelled the dialog")
            return
        chosen_path = e.path
        chosen_path = chosen_path.replace('\\', '')
        if '/Volumes/Google Drive/' in chosen_path:
            chosen_path = chosen_path.replace(
                '/Volumes/Google Drive/', f"{os.path.expanduser('~')}/Google Drive/")
        listener_chose_dir('some topic', {'path': chosen_path,
                                 'news': 'Sold for $1M'})
        # txt1.value = chosen_path
        # txt1.update()
        # model_add_favourite_path(chosen_path)
        # print('chosen_path AFTER dir selection', chosen_path)
        # button_scan_clicked(None)

    def button_scan_png_clicked(e):

        def chose_png(e):
            value = e.control.data  # easier communication with button handler via 'data' attribute
            # display image of png in value in image control
            full_path = os.path.join(txt1.value, value)
            print('chose', full_path)
            dst = "assets/preview.png"
            shutil.copyfile(full_path, dst)

            # img.src = full_path # this doesn't work?  https://github.com/flet-dev/flet/issues/340 
            # 
            # img.src = f"https://picsum.photos/200/200?{random.randint(0, 1000)}"  # WOKS OK test images.  But not my own images
            # img.src = "/Users/andy/Devel/stable-diffusion-textfile-cleaner/examples/file1_4fbece75_GFPGANv1.3_RealESRGAN_x4plus.png"
            # img.src = "/3961482227_giant_lady_bug__cherries_in_field__by_Darrell_k_sweet_by_hieronymous_Bosch_-gigapixel-art-scale-4_00x.png"
            # img.src = "/Users/andy/Library/Mobile Documents/com~apple~CloudDocs/iCloud Data/AI images created/naked princess hieronymous gen by mac m1 02-gigapixel-art-scale-4_00x.png"
            # img.src = "/naked princess hieronymous gen by mac m1 02-gigapixel-art-scale-4_00x.png"
            # img.src = "/4188317573_giant_lady_bug__cherries_in_field__by_Darrell_k_sweet_by_hieronymous_Bosch_-gigapixel-art-scale-4_00x.png"
            # img.src = "/Users/andy/Library/Mobile Documents/com~apple~CloudDocs/iCloud Data/AI images created/119994449_giant_lady_bug__cherries_in_field__by_Darrell_k_sweet_.png"
            # img.src = "/Users/andy/Library/Mobile Documents/com~apple~CloudDocs/iCloud Data/AI images created/naked princess hieronymous gen by mac m1-gigapixel-art-scale-4_00x.png"
            # img.src = "/Users/andy/Devel/stable-diffusion-textfile-cleaner/examples/2358228892_Fireworks_on_a_giant_mushroom___Oil_painting_intricate_detail__by_Dean_Cornwell_and_Hieronymous_Bosch_and_Matisse_-art-scale-4_00x-gigapixel.png"
            # img.src = "3961482227_giant_lady_bug__cherries_in_field__by_Darrell_k_sweet_by_hieronymous_Bosch_-gigapixel-art-scale-4_00x.png"
            # img.src = "file:///Volumes/SSD/Data/Devel/stable-diffusion-textfile-cleaner/assets/preview.png?{random.randint(0, 1000)}"
            # img.src = "file:///preview.png?{random.randint(0, 1000)}"
            # img.update()
            img.src = "assets/preview.png"
            img.update()

        lv.controls.clear()
        lv.auto_scroll = False
        lv.update()
        png_files = list_png(txt1.value)
        print('png_files', png_files)
        for line in png_files:
            lv.controls.append(
                # TextButton(f"{line}"))
                ElevatedButton(
                content=Row([Text(f"{line}")], alignment="start"),
                width=100,
                on_click=chose_png,
                data=line  # easier communication with button handler
                )
            )
        lv.update()

    def button_scan_clicked(e):
        global bad_txt_files, chosen_path

        lv.controls.clear()
        lv.auto_scroll = False
        lv.update()
        directory = txt1.value
        # check if directory exists
        if not os.path.isdir(directory):
            print(f"directory {directory} does not exist")
            return
        result = list_files(directory)
        set1_txt, set2_png = create_two_sets(result)
        print('text files', set1_txt)
        print('png files', set2_png)
        missing_images = find_missing_files(set1_txt, set2_png)
        print('bad orphans', missing_images)
        print('chosen_path', chosen_path)
        if not chosen_path:
            raise Exception(
                'no path chosen - probably an initialisation error')
        bad_txt_files = add_dir_root_and_txt_extension(
            missing_images, dir=chosen_path)
        print(len(bad_txt_files), 'bad txt files')

        for line in bad_txt_files:
            lv.controls.append(
                Text(f"{line}", size=12, font_family="Consolas", selectable=True))
        lv.update()

        txt2.value = num_orphans_calc()
        txt2.update()

    file_picker = FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    pr = ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def pick_directory(_):
        pr.visible = True
        page.update()

        file_picker.initial_directory = model_get_initial_directory()
        file_picker.get_directory_path()
        sleep(3)

        pr.visible = False
        page.update()

    btnPick = ElevatedButton("Choose DIR...",
                             #  on_click=lambda _: file_picker.get_directory_path())
                             on_click=pick_directory)
    btnPickFav = ElevatedButton("Choose Fav...",
                              on_click=lambda _: choose_favourite(None))
    last_favourite_dir = chosen_path = model_get_last_favourite_dir()
    txt1 = TextField(label="DIR", value=last_favourite_dir, expand=True)

    dd = Dropdown(
        width=100,
        options=[
            dropdown.Option("Red"),
            dropdown.Option("Green"),
            dropdown.Option("Blue"),
        ],
    )
    for fav in model_get_last_favourites():
        dd.options.append(dropdown.Option(fav))

    btnScan = FilledTonalButton(
        "List Orphan .txt", icon=icons.FIND_IN_PAGE, on_click=button_scan_clicked)
    btnScanPng = FilledTonalButton(
        "List .png", icon=icons.FIND_IN_PAGE, on_click=button_scan_png_clicked)
    row = Row(spacing=0, controls=[
              btnPick,
              btnPickFav,
              pr,
              txt1,
              # dd, # if want to display dropdown
              btnScan,
              btnScanPng
              ],
              alignment="start")
    page.add(row)

    def buttonDelete_clicked(e):
        lv.controls.clear()
        lv.auto_scroll = True
        num_left_to_delete = len(bad_txt_files)
        for file_path in bad_txt_files:
            if not os.path.exists(file_path):
                print('  File does not exist', file_path)
            else:
                deleted_msg = f"Deleted {file_path}"
                print(deleted_msg)
                # os.remove(file_path)
                lv.controls.append(Text(
                    deleted_msg, size=12, font_family="Consolas", color="red600", selectable=True))
                num_left_to_delete -= 1

                txt2.value = num_orphans_calc(num_left_to_delete)
                txt2.update()
            lv.update()

    def num_orphans_calc(num=None):
        if num is None:
            num = len(bad_txt_files)
        return f"{num} orphaned text files"

    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
    # img = Image(
    #     # src=f"./examples/file2_5fbece75_RealESRGAN_x4plus.png",
    #     src=f"/Users/andy/Devel/stable-diffusion-textfile-cleaner/examples/file2_5fbece75_RealESRGAN_x4plus.png",
    #     # width=100,
    #     # height=100,
    #     # fit="contain",
    #     tooltip="Image",
    # )
    i = random.randint(1, 1000)
    img = Image( src=f"https://picsum.photos/200/200?{i}", width=500, height=500, )
    # Must put the ListView in a Container with a size, otherwise listview will be 0 size and not seen
    c1 = Container(
        content=lv,
        # bgcolor=colors.GREEN,
        width=700,
        height=500,
        padding=5,
    )
    # page.add(img)
    # page.add(lv)
    row = Row(spacing=0, controls=[
            c1,
            img,
            ], alignment="center")
    page.add(row)

    btnDeleteOrphans = ElevatedButton(f"Delete Orphans", icon=icons.DELETE, on_click=buttonDelete_clicked, style=ButtonStyle(
        bgcolor={"focused": colors.RED_200, "": colors.RED_900},
    ))
    txt2 = Text(value=num_orphans_calc(), expand=False)
    container_4 = Container(content=txt2, padding=padding.only(left=10))
    row_prefs = Row(spacing=0, alignment="end", expand=True, controls=[
                    ElevatedButton("Preferences...", icon=icons.SETTINGS, on_click=edit_preferences)])
    row = Row(spacing=0, controls=[
              btnDeleteOrphans,
              container_4,
              row_prefs,
              ], alignment="center")
    page.add(row)

    def on_keyboard(e: KeyboardEvent):
        # keypressed = f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}"
        # print (keypressed)
        if e.key == ',' and e.meta:
            edit_preferences(None)

    page.on_keyboard_event = on_keyboard

    page.update()

    # preferences.set_page(page)
    # choose_favourites.set_page(page)


flet.app(target=main, assets_dir="assets")
# flet.app(target=main)
# flet.app(target=main, view=flet.WEB_BROWSER)

