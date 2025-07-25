import argparse
import os
import pathlib
import sys

import numpy as np
import pandas as pd
from data_analysis import analyze_df
from predictions import predict
from read_data import Data
from video_analysis import analysis


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--rmin',
        default = 72, 
        help = 'Minimum radius of the well'
        )
    parser.add_argument(
        '--rmax', 
        default = 100, 
        help = 'Maximum radius of the well'
        )
    parser.add_argument(
        '--experiment_dir', 
        type=str, 
        help = "which folder would you like to analyze"
        )
    parser.add_argument(
        '--model_name', 
        type=str, 
        help = "name of the model you want to use"
        )
    parser.add_argument(
        '--starting_image', 
        default=0, 
        type=int, 
        help = "Index for the starting image",
        required = False
        )

    return parser.parse_args()

if __name__ =='__main__':
    try:
    
        user = os.getenv("USER")
        data_dir = "/users"
    
        args = parse_arguments()
        rmin = args.rmin
        rmax = args.rmax
        experiment_dir = args.experiment_dir
        model_name = args.model_name
        starting_image = args.starting_image
    
        image_folder = os.path.join(data_dir, user, experiment_dir)
    
        images = Data(image_folder + '/IMG_%04d.JPG')
        results_file = image_folder + '/results.csv'
        img_file = image_folder + '/wells.png'
    
        model_path = os.path.join(pathlib.Path(__file__).parent.absolute(), '../model_zoo', model_name)
    
        experiment = analysis(images)
        infer = predict(images, experiment, model_path)
    
        print("Loading images ...")
    
        images = Data(image_folder + '/IMG_%04d.JPG')
    
        ret, image, _ = images.read()
        if not ret:
            print("Images could not be loaded. Possible reasons")
            print("1. Images are directly not under this folder. If so please provide the folder where the images are stored")
            print("2. Images are not named IMG_%04d.JPG -> first image = IMG_0001.JPG, 1400th image = IMG_1400.JPG .")
            print("Closing this session. Please launch again with recommended changes")
            sys.exit()
    
        images.reset()
    
        wells = experiment.detect_wells(R = [rmin, rmax])
    
        experiment.plot_wells(wells = wells, img_file = img_file, R = [rmin, rmax])
    
        print("Total number of wells detected = {}".format(len(wells)), flush = True)
    
        print("Running predictions. This will take a while!", flush = True)
    
        
        predictions = infer.predict(wells = wells)
    
        print("Analyzing and writing results to " + results_file, flush = True)
    
        observations = analyze_df(predictions, wells, starting_image)
        observations.to_csv(results_file)

        print("Completed job!", flush = True)
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print("Script failed with error:\n", error_msg)

