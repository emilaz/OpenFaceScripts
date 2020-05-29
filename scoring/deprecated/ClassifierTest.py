"""
This file is to test a trained classifier on a previously unseen patient.
Note: more or less deprecated, but useful functions if need for revival.
"""

from scoring.EmotionPredictor import make_emotion_data, conf_mat, score_heatmap
import dask.dataframe as dd
import random
import glob
from dask.distributed import Client

import threading
import pickle
import functools
from pathos.multiprocessing import ProcessingPool as Pool
import os
from tqdm import tqdm
import sys
import multiprocessing
from sklearn import metrics
import pandas as pd

if __name__ == '__main__':
    # patient = sys.argv[sys.argv.index('-p') + 1]
    # pat_dir = sys.argv[sys.argv.index('-d') + 1]
    classifier = sys.argv[sys.argv.index('-c') + 1]
    # os.chdir(pat_dir)
    # here are the steps:
    # 1. load patient data
    # PATIENT_DIRS = [
    #     x for x in glob.glob('*cropped') if 'hdfs' in os.listdir(x) and patient in x
    #     # this returns only the patient we're looking for (all sessions and vid)
    # ]
    # patient_queue = multiprocessing.Manager().Queue()
    # partial_patient_func = functools.partial(load_patient, patient_queue)
    # max_ = len(PATIENT_DIRS)
    #
    # with Pool() as p:
    #     with tqdm(total=max_) as pbar:
    #         for i, _ in enumerate(p.imap(partial_patient_func, PATIENT_DIRS[:max_], chunksize=100)):
    #             pbar.update()
    #
    # ###
    # dask_hdfs = dump_queue(patient_queue)
    # pd_hdfs = [d.compute() for d in dask_hdfs]
    # df = pd.concat(pd_hdfs)
    # df = dd.from_pandas(df, chunksize=5000)
    ###


    # 2.load trained classifier
    print('load classifier')
    rf_classifier = pickle.load(open(classifier, 'rb'))
    
    client = Client(processes=False)
    print(client)
    df = dd.read_hdf('/home/emil/openface_output/all_aus/au_*.hdf', '/data')
    print('Files read')

    feat, label, _ = make_emotion_data('Happy',df)

    # 3. apply classifier to data, record result
    print('predict')
    predicted = rf_classifier.predict(feat)
    #4. write to file
    print('write')
    f = open('/home/emil/openface_output/all_aus/test_on_all.txt', 'w')
    f.write("Results on separate patient (not seen during training):\n%s\n" %
              (metrics.classification_report(label, predicted)))
    f.write("Confusion matrix:\n%s\n" % metrics.confusion_matrix(
        label, predicted))
    conf_mat(predicted, label, 'Confusion Matrix on All Data')
    score_heatmap(predicted, label, 'Classification Metrics on All Data')
    f.close()
    quit()