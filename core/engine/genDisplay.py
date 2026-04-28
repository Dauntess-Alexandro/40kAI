import imageio
import os
from tqdm import tqdm
import numpy as np
from project_paths import ARTIFACTS_METRICS_DIR, RUNTIME_STATE_DIR

def makeGif(numOfLife, name="", Type = "train", trunc = False):
    print("\nForging model_train.gif...\n")
    images = []

    savePath = "display/"
    if not os.path.isdir(savePath):
        os.makedirs(savePath, exist_ok=True)
        print(
            "genDisplay.makeGif: папка display/ не найдена, создана автоматически. "
            "Что делать: убедитесь, что рендер включён и кадры записываются."
        )

    files = os.listdir(savePath)
    files = [os.path.join(savePath, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))

    if trunc == True:
        if numOfLife > 1:
            its = np.arange(1, numOfLife)
            sample_size = min(30, len(its))
            itsChosen = np.random.choice(its, sample_size, replace=False)
        else:
            itsChosen = np.array([], dtype=int)
        newFiles = []
        print(itsChosen)

        for i in files:
            for j in itsChosen:
                digits = len(str(j))
                print()
                if i[:9+digits] == "display/{}_".format(j):
                    newFiles.append(i)
        files = newFiles
        print(files)

    if not files:
        print(
            "genDisplay.makeGif: нет кадров для гифки в display/. "
            "Причина: папка пуста или фильтр trunc отсеял все файлы. "
            "Что делать: убедитесь, что в display/ есть кадры и numOfLife > 1."
        )
        return


    for fil in tqdm(files):
        images.append(imageio.imread(fil))
    if not images:
        print(
            "genDisplay.makeGif: не удалось собрать кадры для гифки. "
            "Что делать: проверьте читаемость файлов в display/."
        )
        return
    if Type == "train":
        img_dir = os.path.join(str(RUNTIME_STATE_DIR), "img")
        build_img_dir = os.path.join(str(RUNTIME_STATE_DIR), "build", "img")
        debug_img_dir = os.path.join(str(RUNTIME_STATE_DIR), "build", "Debug", "img")
        os.makedirs(str(ARTIFACTS_METRICS_DIR), exist_ok=True)
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(build_img_dir, exist_ok=True)
        os.makedirs(debug_img_dir, exist_ok=True)
        imageio.mimsave(os.path.join(str(ARTIFACTS_METRICS_DIR), 'model_train{}.gif'.format(name)), images)
        imageio.mimsave(os.path.join(img_dir, 'model_train{}.gif'.format(name)), images)
        imageio.mimsave(os.path.join(build_img_dir, 'model_train{}.gif'.format(name)), images)
        imageio.mimsave(os.path.join(debug_img_dir, 'model_train{}.gif'.format(name)), images)
    elif Type == "val":
        os.makedirs("val", exist_ok=True)
        imageio.mimsave('val/model_val.gif', images)
    print("Generated gif")
