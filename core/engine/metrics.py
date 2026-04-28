import matplotlib.pyplot as plt
import numpy as np
import json
import os
from scipy.optimize import curve_fit
from project_paths import ARTIFACTS_METRICS_DIR, ARTIFACTS_MODELS_DIR, RUNTIME_STATE_DIR

class metrics(object):
    def __init__(self, folder, randNum, modelName):
        self.avgRew = []
        self.loss = []
        self.episodeLen = {"labels": [], "vals": []}
        self.folder = folder
        self.randNum = randNum
        self.modelName = modelName
        self.metrics_dir = str(ARTIFACTS_METRICS_DIR)
        self.img_dir = os.path.join(str(RUNTIME_STATE_DIR), "img")
        self.models_dir = str(ARTIFACTS_MODELS_DIR)
        os.makedirs(self.metrics_dir, exist_ok=True)
        os.makedirs(self.img_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)

    def updateRew(self, add):
        self.avgRew.append(add)

    def updateLoss(self, add):
        self.loss.append(add)

    def updateEpLen(self, add):
        self.episodeLen["vals"].append(add)
        self.episodeLen["labels"].append(str(add))

    def lossCurve(self):
        plt.title("Loss Curve")
        plt.xlabel("Counts")
        plt.ylabel("Loss")
        plt.plot(self.loss)

        plt.savefig(os.path.join(self.metrics_dir, "loss_{}.png".format(self.randNum)))
        plt.savefig(os.path.join(self.img_dir, "loss.png"))
        plt.savefig(os.path.join(self.img_dir, "loss_{}.png".format(self.randNum)))
        plt.close()

    def showRew(self):
        y = lambda x,a,b: a * x + b
        x = np.arange(len(self.avgRew))
        popt, _ = curve_fit(y, x, self.avgRew)
        a, b = popt

        plt.title("Avg. Reward per Episode")
        plt.xlabel("Episodes")
        plt.ylabel("Reward")
        plt.plot(self.avgRew)
        plt.plot(x, y(x, a, b))

        plt.savefig(os.path.join(self.metrics_dir, "reward_{}.png".format(self.randNum)))
        plt.savefig(os.path.join(self.img_dir, "reward.png"))
        plt.savefig(os.path.join(self.img_dir, "reward_{}.png".format(self.randNum)))
        plt.close()

    def showEpLen(self):
        plt.title("Episode Length")
        plt.xlabel("Episodes")
        plt.ylabel("Episode Len")
        plt.bar(self.episodeLen["labels"], self.episodeLen["vals"])

        plt.savefig(os.path.join(self.metrics_dir, "epLen_{}.png".format(self.randNum)))
        plt.savefig(os.path.join(self.img_dir, "epLen.png"))
        plt.savefig(os.path.join(self.img_dir, "epLen_{}.png".format(self.randNum)))
        plt.close()

    def createJson(self):
        data = {"loss":"img/loss_{}.png".format(self.randNum), 
        "reward":"img/reward_{}.png".format(self.randNum), 
        "epLen":"img/epLen_{}.png".format(self.randNum), 
        "winrate": "img/winrate_{}.png".format(self.randNum),
        "vpdiff": "img/vpdiff_{}.png".format(self.randNum),
        "endreasons": "img/endreasons_{}.png".format(self.randNum),}

        with open(os.path.join(self.models_dir, "data_{}.json".format(self.modelName)), "w") as f:
            json.dump(data, f)
