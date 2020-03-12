from pycocotools.coco import COCO
import pycocotools.mask as rletools
from pycocotools.mask import toBbox
from pycocotools.mask import decode
from pycocotools.mask import encode
import numpy as np
import glob
import matplotlib.pyplot as plt
import pylab
import os
import pickle
from detectron2.structures import BoxMode


def generate_dataset_dicts(text_instances, server):
    """ Generates the dataset in COCO format """

    dataset_dicts = []
    dataset_dicts = []

    for text_file in text_instances:
        folder = text_file.split('/')[-2]

        frame_index = 0
        with open(text_file, 'r') as f:
            lines = f.readlines()
        f.close()
        objects = []
        record = {}
        
        lines_id = 0
        for line in lines:
            fields = line.split(' ')
            time_frame = fields[0]
            object_id = fields[1]
            class_id = fields[2]
            img_height = fields[3]
            img_width = fields[4]
            rle = fields[5].split('\n')[0]

            decode_obj = {'size': [int(img_height), int(img_width)],
                        'counts': rle
            }
            bbox = toBbox(decode_obj)

            if lines_id == 0:
                if server:
                    record['file_name'] = '../mcv/datasets/KITTI-MOTS/training/images_02/' + folder + '/' + str(frame_index).zfill(6)
                else:
                    record['file_name'] = '../KITTI-MOTS/training/images_02/' + folder + '/' +str(frame_index).zfill(6)
                record['image_id'] = frame_index
                record['height'] = img_height
                record['width'] = img_width

            if int(time_frame) != frame_index:
                record["annotations"] = objects
                dataset_dicts.append(record)

                frame_index += 1
                record = {}
                objects = []

                if server:
                    record['file_name'] = '../mcv/datasets/KITTI-MOTS/training/images_02/' + folder + '/' + str(frame_index).zfill(6) + '.png'
                else:
                    record['file_name'] = '../KITTI-MOTS/training/images_02/' + folder + '/' +str(frame_index).zfill(6) + '.png'
                record['image_id'] = frame_index
                record['height'] = img_height
                record['width'] = img_width
            
            if int(class_id) != 10:
                obj = {
                        "bbox": bbox,
                        "bbox_mode": BoxMode.XYXY_ABS,
                        "category_id": int(class_id)
                }
                objects.append(obj)
            lines_id += 1

    return dataset_dicts


def main():
    train_dataset_dicts = []
    val_dataset_dicts = []

    train_folders = []

    text_instances = glob.glob('../KITTI-MOTS/instances_txt/*.txt')
    text_instances.sort()

    train_text_instances = []
    val_text_instances = []
    val_folders = ['0002', '0006', '0007', '0008', '0010', '0013', '0014', '0016', '0018']

    for text_instance in text_instances:
        if text_instance.split('/')[-1].split('.')[0] in val_folders:
            val_text_instances.append(text_instance)
        else:
            train_text_instances.append(text_instance)

    local_train_dict = generate_dataset_dicts(train_text_instances, False)
    local_val_dict = generate_dataset_dicts(val_text_instances, False)
    server_train_dict = generate_dataset_dicts(train_text_instances, True)
    server_val_dict = generate_dataset_dicts(val_text_instances, True)

    with open('./train_kitti_mots_dataset_server.pkl', 'wb') as handle:
        pickle.dump(server_train_dict, handle)
    handle.close()

    with open('./validation_kitti_mots_dataset_server.pkl', 'wb') as handle:
        pickle.dump(server_val_dict, handle)
    handle.close()

    with open('./train_kitti_mots_dataset_local.pkl', 'wb') as handle:
        pickle.dump(local_train_dict, handle)
    handle.close()

    with open('./validation_kitti_mots_dataset_local.pkl', 'wb') as handle:
        pickle.dump(local_val_dict, handle)
    handle.close()


if __name__ == '__main__':
    main()





        
        
    # for line in lines:
    #     line_elements = line.split(" ")

    #     if int(line_elements[0]) != frame_index:
    #         frame = cv2.imread(filenames[frame_index])
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #         if brake:
    #             time_start = time.time()
    #             _ = brake_light_detector.detect(frame, vehicles_info)
    #             time_end = time.time()
    #             print('Frame processing time: ', time_end - time_start)
    #         if turning:
    #             time_start = time.time()
    #             _ = turn_light_detector.detect(frame, vehicles_info)
    #             time_end = time.time()
    #             print('Frame processing time: ', time_end - time_start)
    #         vehicles_info = []
    #         frame_index += 1

    #     if line_elements[2] in vehicles:
    #         vehicle_info = {}

    #         # Get the bounding box points from the text file
    #         vehicle_pt1 = (int(float(line_elements[6])), int(float(line_elements[7])))
    #         vehicle_pt2 = (int(float(line_elements[8])), int(float(line_elements[9])))
    #         # Get the vehicle_id
    #         vehicle_id = line_elements[1]
    #         alpha, rotation_y = line_elements[5], line_elements[16]
    #         beta = float(alpha)*-1.0 -2*math.pi + float(rotation_y)*-1.0
    #         contrabeta = np.arctan(float(line_elements[15])/float(line_elements[13]))

    #         vehicle_info['bbox'] = (vehicle_pt1, vehicle_pt2)
    #         vehicle_info['vehicle_id'] = vehicle_id
    #         vehicle_info['vehicle_angle_information'] = {'alpha': alpha,
    #                                                     'beta': beta,
    #                                                     'rotation_y': rotation_y,
    #                                                     'contrabeta': contrabeta}
    #         vehicle_info['occlusion'] = int(line_elements[4])

    #         vehicles_info.append(vehicle_info)
