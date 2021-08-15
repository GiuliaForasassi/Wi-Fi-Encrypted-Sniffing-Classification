import pyshark
import glob # guarda i files dentro la cartella
import time
import numpy as np
from numpy import var
from collections import Counter

sub_directories = ['emails', 'video', 'videocalls', 'webpages']
total_features = []
total_labels = []

MAC_SNIFFED_PC = '34:7d:f6:e2:87:81'
MAC_ROUTER = '74:36:6d:ab:43:c4'

# load files
for subdirectory in sub_directories:

    for name in glob.glob('captures/' + subdirectory + '/*.pcapng'):
        t1 = time.perf_counter()
        file = pyshark.FileCapture(name, use_json=True)

        lengths_upload = []
        lengths_download = []

        inter_arrival_times_upload = []
        inter_arrival_times_download = []

        relative_times = []
        types = []
        t2 = time.perf_counter()
        print('lettura file', t2-t1)
        # features extraction
        for p, packet in enumerate(file):

            length = int(packet.length)
            inter_arrival_time = float(packet.frame_info.time_delta)
            relative_time = float(packet.frame_info.time_relative)

            if packet.wlan.ta == MAC_SNIFFED_PC and packet.wlan.ra == MAC_ROUTER:  # --> upload
                # list of lengths of one file
                lengths_upload.append(length)
                # list of inter arrival times of one file
                inter_arrival_times_upload.append(inter_arrival_time)
            elif packet.wlan.ta == MAC_ROUTER and packet.wlan.ra == MAC_SNIFFED_PC: # --> download
                lengths_download.append(length)
                inter_arrival_times_download.append(inter_arrival_time)
            else:
                print('continue')
                continue

            relative_times.append(relative_time)
            # types.append(int(packet.wlan.fc_type))
            types.append(int(packet.wlan.fc_tree.type))

            # if p == 500:
            #     break

        t3 = time.perf_counter()
        print('ciclo for', t3 - t2)

        total_length_upload = sum(lengths_upload)
        total_length_download = sum(lengths_download)

        avg_inter_arrival_time_upload = sum(inter_arrival_times_upload) / len(inter_arrival_times_upload)
        avg_inter_arrival_time_download = sum(inter_arrival_times_download) / len(inter_arrival_times_download)

        min_inter_arrival_time_upload = min(inter_arrival_times_upload)
        min_inter_arrival_time_download = min(inter_arrival_times_download)

        max_inter_arrival_time_upload = max(inter_arrival_times_upload)
        max_inter_arrival_time_download = max(inter_arrival_times_download)

        var_inter_arrival_time_upload = var(inter_arrival_times_upload)
        var_inter_arrival_time_download = var(inter_arrival_times_download)

        flow_time = max(relative_times)

        c = Counter(types)
        number_management_type = c[0]
        number_control_type = c[1]
        number_data_type = c[2]

        percentage_management_type = (number_management_type * 100)/len(types)
        percentage_control_type = (number_control_type * 100) / len(types)
        percentage_data_type = (number_data_type * 100) / len(types)


        features = [total_length_upload, total_length_download, avg_inter_arrival_time_upload, avg_inter_arrival_time_download,
                      flow_time, min_inter_arrival_time_upload, min_inter_arrival_time_download, max_inter_arrival_time_upload, max_inter_arrival_time_download,
                    percentage_management_type, percentage_control_type, percentage_data_type]
        total_features.append(features)
        total_labels.append(sub_directories.index(subdirectory))

        file.close()
        t4 = time.perf_counter()
        print('features', t4 - t3)

print(total_features)
print(total_labels)

X = np.array(total_features)
y = np.array(total_labels)

# DATASET CREATION WITH PICKLE
with open('dataset.npy', 'wb') as f:
    np.save(f, X)
    np.save(f, y)