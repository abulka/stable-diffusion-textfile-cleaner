from time import sleep
import flet
from flet import ListView, Page, Text
from main import list_files, create_two_sets, find_missing_files, add_txt_extension, DIR

def main(page: Page):
    page.title = "Auto-scrolling ListView"

    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    count = 1

    result = list_files(DIR)
    set1_txt, set2_png = create_two_sets(result)
    # print(result)
    print('text files', set1_txt)
    print('png files', set2_png)
    missing_images = find_missing_files(set1_txt, set2_png)
    print('bad orphans', missing_images)
    bad_txt_files = add_txt_extension(missing_images)
    print(len(bad_txt_files), 'bad txt files')

    for line in bad_txt_files:
        lv.controls.append(Text(f"{line}"))
        count += 1

    page.add(lv)

    # for i in range(0, 60):
    #     sleep(1)
    #     lv.controls.append(Text(f"Line {count}"))
    #     count += 1
    #     page.update()

flet.app(target=main)
