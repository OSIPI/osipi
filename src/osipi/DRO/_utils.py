import os

import numpy as np
import pydicom
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_mri(slices, mode="time", slice_index=0, time_index=0):
    fig, ax = plt.subplots()
    if mode == "time":
        frames = slices.shape[-1]

        def init():
            ax.imshow(slices[:, :, slice_index, 0], cmap="gray")
            ax.set_title(f"Slice: {slice_index}, Time: 0")

        def animate(t):
            ax.clear()
            ax.imshow(slices[:, :, slice_index, t], cmap="gray")
            ax.set_title(f"Slice: {slice_index}, Time: {t}")

    elif mode == "slice":
        frames = slices.shape[2]

        def init():
            ax.imshow(slices[:, :, 0, time_index], cmap="gray")
            ax.set_title(f"Slice: 0, Time: {time_index}")

        def animate(z):
            ax.clear()
            ax.imshow(slices[:, :, z, time_index], cmap="gray")
            ax.set_title(f"Slice: {z}, Time: {time_index}")

    anim = FuncAnimation(
        fig=fig, func=animate, frames=frames, init_func=init, interval=100, blit=False
    )
    plt.show()
    return anim


def save_dicoms(outdir, original_dicom, signal, patient_id_num, study_instance_uid):
    new_dicoms = original_dicom.copy()
    patient_id_num = "RIDER Neuro MRI-{}".format(patient_id_num)

    uidprefix = "1.3.6.1.4.1.9328.50.16."

    SeriesInstanceUID = pydicom.uid.generate_uid(prefix=uidprefix)
    StorageMediaFileSetUID = pydicom.uid.generate_uid(prefix=uidprefix)
    FrameOfReferenceUID = pydicom.uid.generate_uid(prefix=uidprefix)
    SeriesID = SeriesInstanceUID[-5:]
    Seriesdir = "{}.000000-perfusion-{}".format(original_dicom[0][0].SeriesNumber, SeriesID)
    StudyDate = "19040323"
    DateID = study_instance_uid[-5:]
    Datedir = "23-03-1904-BRAINRESEARCH-{}".format(DateID)

    if not os.path.exists(outdir):
        os.makedirs("{}/{}/{}/{}".format(outdir, patient_id_num, Datedir, Seriesdir))

    z = 0
    for entries in new_dicoms:
        t = 0
        for snap in new_dicoms[z]:
            SOPInstanceUID = pydicom.uid.generate_uid(prefix=uidprefix)
            snap.PatientID = patient_id_num
            snap.SOPInstanceUID = SOPInstanceUID
            snap.StudyInstanceUID = study_instance_uid
            snap.SeriesInstanceUID = SeriesInstanceUID
            snap.StorageMediaFileSetUID = StorageMediaFileSetUID
            snap.FrameOfReferenceUID = FrameOfReferenceUID
            snap.StudyDate = StudyDate
            snap.ContentDate = StudyDate
            Sout = abs(signal[:, :, z, t])
            Sout = Sout.astype(np.uint16)
            snap.PixelData = Sout.tobytes()
            fname = str(t + 1).zfill(2) + "-" + str(z + 1).zfill(4)
            snap.save_as(
                "{}/{}/{}/{}/{}.dcm".format(outdir, patient_id_num, Datedir, Seriesdir, fname),
                write_like_original=False,
            )
            t += 1
        z += 1
    return
