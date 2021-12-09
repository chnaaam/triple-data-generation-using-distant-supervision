import os
import shutil
from tqdm import tqdm
from config import load_config


def main():
    config = load_config(path="./data.cfg")

    page_list = os.listdir(config.page_filtering.path.pages)

    for file_name in tqdm(page_list):
        title = file_name.replace(".txt", "")

        if title[0] == "%" and title[-1] == "%":
            continue

        if len(title) == 1:
            continue

        if title[0] in "!@#$%^&*-_=+~`.\'\" 0123456789":
            continue

        if title.split("_")[0].upper() != title.split("_")[0].lower():
            continue

        if title.upper() != title.lower():
            continue

        shutil.copy(
            os.path.join(config.page_filtering.path.pages, file_name),
            os.path.join(config.page_filtering.path.filtered_pages, file_name)
        )

if __name__ == "__main__":
    main()