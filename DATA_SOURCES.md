# Dataset source audit

## Adopted now

### GMDCSA24 - train/validation/internal test

- Source: author repository, `ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos`.
- License in repository: MIT.
- Local verification: 160 MP4 videos, 4 subject directories, 81 ADL and 79 fall videos, 1.03 GiB of video data.
- Protocol: four subject-independent folds. In each fold one subject is test, the next subject is validation, and the other two are training.

### MCFD - external cross-view test

- Original source: Universite de Montreal, 24 scenarios recorded from 8 camera views.
- Original site currently blocks automated downloads; Kaggle mirror is used only as transport.
- Integrity gate: the archive must extract to 24 scenarios and 192 camera-view videos before it is accepted.
- Protocol in this project: no MCFD camera is used for model training. Cam1 is used only for an optional threshold-calibration experiment, cam3 is development observation, and cameras 2/4/5/6/7/8 form the frozen cross-view external test.
- Annotation coverage: the supplied segment table covers scenarios 1-23; scenario 24 videos are retained but excluded because no matching segment annotation is available.
- Local audit: 552 unique segments referencing 184 videos, with no missing files or out-of-range intervals. One obvious `cam55` typo was corrected to the existing `cam5` file and recorded in `data/splits/mcfd_binary_cross_view/audit.json`.

## Rejected candidate

### Kaggle HAR-UP Fall Dataset (`pragyachandak/upfalldataset`)

- Downloaded archive SHA-256: `BEB4EB1A3358D35182991F784F6DDA3E4CD35CAF3024370FCFD9DF432EE28DC0`.
- Contents: one 78.4 MiB CSV (`CompleteDataSet (1).csv`), no RGB images or videos.
- Kaggle metadata license: Unknown.
- Decision: not usable for YOLO-Pose or RTMPose and excluded from training.

## Deferred

### Official UP-Fall vision data

- The official project states that camera data is distributed per subject/activity/trial and that no single complete image archive is provided.
- The full multimodal release is hundreds of gigabytes; compact third-party copies must not be accepted without subject, camera, trial, timestamp, provenance, and license verification.
- It can be added later as an expansion dataset without changing the shared pose-cache or evaluation formats.
