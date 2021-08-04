import pyshark
import glob # guarda i files dentro la cartella

sub_directories = ['emails', 'video', 'videocalls', 'webpages']
total_features = []
total_labels = []

MAC_SNIFFED_PC = '34:7d:f6:e2:87:81'

# load files
for subdirectory in sub_directories:

    for name in glob.glob('captures2/' + subdirectory + '/*.pcapng'):
        file = pyshark.FileCapture(name)

        lengths_upload = []
        lengths_download = []

        inter_arrival_times_upload = []
        inter_arrival_times_download = []

        relative_times = []

        # features extraction
        for packet in file:
            length = int(packet.length)
            inter_arrival_time = float(packet.frame_info.time_delta)
            relative_time = float(packet.frame_info.time_relative)

            relative_times.append(relative_time)
            # --> upload
            if packet.wlan.ta == MAC_SNIFFED_PC:
                # list of lengths of one file
                lengths_upload.append(length)
                # list of inter arrival times of one file
                inter_arrival_times_upload.append(inter_arrival_time)
            else:
                lengths_download.append(length)
                inter_arrival_times_download.append(inter_arrival_time)


        # first feature: total length
        total_length_upload = sum(lengths_upload)
        total_length_download = sum(lengths_download)
        # second feature: average of inter arrival times
        avg_inter_arrival_time_upload = sum(inter_arrival_times_upload) / len(inter_arrival_times_upload)
        avg_inter_arrival_time_download = sum(inter_arrival_times_download) / len(inter_arrival_times_download)
        # third feature: maximum of the absolute times
        flow_time = max(relative_times)


        features = [total_length_upload, total_length_download, avg_inter_arrival_time_upload, avg_inter_arrival_time_download,
                    flow_time]
        total_features.append(features)
        total_labels.append(sub_directories.index(subdirectory))

        file.close()

print(total_features)
print(total_labels)

