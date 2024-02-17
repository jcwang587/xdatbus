import os
import shutil
import matplotlib.pyplot as plt
import numpy as np


def gauss_pot(x, x0, h, w):
    en = h * np.exp(-((x - x0) ** 2) / 2.0 / w**2)
    return en


def calculate_profile_1d(server_meta_path, project_name, input_line_number):
    server_hillspot_path = server_meta_path + project_name + "/HILLSPOT"

    local_hillspot_path = "./hillspot_files"

    # Copy the hillspot files to local
    if os.path.exists(local_hillspot_path):
        shutil.rmtree(local_hillspot_path)
    os.mkdir(local_hillspot_path)
    shutil.copy(server_hillspot_path, local_hillspot_path)

    f = local_hillspot_path + "/HILLSPOT"
    ff = f + ".xyz"

    a0 = -1.0
    a1 = 2.0
    num = 1000

    f = open(f, "r")

    data = []
    h = []
    w = []
    step = 0
    for line in f.readlines():
        line = line.split()
        x = []
        if len(line) > 2:
            for i in range(len(line) - 2):
                x.append(float(line[i]))
            data.append(x)
            h.append(float(line[-2]))
            w.append(float(line[-1]))
        step += 1
        if step > input_line_number:
            break
    f.close()

    ff = open(ff, "w")
    step = (a1 - a0) / num
    x = a0
    for i in range(1, num):
        en = 0.0
        x = x + step
        for j in range(len(data)):
            x0 = data[j][0]
            en_ = gauss_pot(x, x0, h[j], w[j])
            en += en_
        ff.write(repr(x) + "\t" + repr(-en) + "\n")
    ff.close()

    return data


def plot_profile(server_path, project_path):
    # clear and create output directory
    if os.path.exists("./output_" + project_path + "_all"):
        shutil.rmtree("./output_" + project_path + "_all")
    os.mkdir("./output_" + project_path + "_all")

    # get the length of hillspot file
    f = server_path + project_path + "/HILLSPOT"
    f = open(f, "r")
    input_line_number = 0
    for _ in f.readlines():
        input_line_number += 1
    print("input_line_number = ", input_line_number)

    # calculate the profile
    calculate_profile_1d(server_path, project_path, input_line_number)

    # read the hillspot.xyz file two column data
    hillspotxyz_path = "./hillspot_files/HILLSPOT.xyz"
    hillspotxyz = np.loadtxt(hillspotxyz_path, usecols=(0, 1))

    # wrap the hillspotxyz into 0-1
    third_point = len(hillspotxyz) // 3
    hillspotxyz_p1 = hillspotxyz[0:third_point, 1]
    hillspotxyz_p2 = hillspotxyz[third_point : 2 * third_point, 1]
    hillspotxyz_p3 = hillspotxyz[2 * third_point :, 1]
    hillspotxyz_ppp = hillspotxyz_p1 + hillspotxyz_p2 + hillspotxyz_p3
    hillspotxyz_wrap = hillspotxyz.copy()[third_point : 2 * third_point, :]
    hillspotxyz_wrap[:, 1] = hillspotxyz_ppp

    # Select the data for plot
    hillspotxyz_plot = hillspotxyz_wrap.copy()
    # Subtract the maximum value
    hillspotxyz_plot[:, 1] = hillspotxyz_plot[:, 1] - min(hillspotxyz_plot[:, 1])

    return hillspotxyz_plot


def plot_cv(server_path, project_path, idx):
    # clear and create output directory
    if os.path.exists("./output_" + project_path + "_all"):
        shutil.rmtree("./output_" + project_path + "_all")
    os.mkdir("./output_" + project_path + "_all")

    # get the length of hillspot file
    f = server_path + project_path + "/HILLSPOT"
    f = open(f, "r")
    input_line_number = 0
    for _ in f.readlines():
        input_line_number += 1
    print("input_line_number = ", input_line_number)

    # calculate the profile
    cv = calculate_profile_1d(server_path, project_path, input_line_number)
    cv = sum(cv, [])
    print(cv)
    # plot the cv
    plt.plot([float(x) * 200 / 1000 for x in range(len(cv))], cv, "-")
    plt.legend([project_path], loc="upper left")
    print("project_path = ", project_path)
    if idx == 3:
        plt.xlabel("Time (ps)")
    plt.ylabel("CV")
