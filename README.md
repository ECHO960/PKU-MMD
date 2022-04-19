# PKU-MMD: A Large Scale Benchmark for Continuous Multi-Modal Human Action Understanding

<div align=center >
 
 [Spatial and Temporal Resolution Up Conversion Team, ICST, Peking University](http://www.icst.pku.edu.cn/struct)</br>
This dataset is partially funded by Microsoft Research Asia, project ID FY17-RES-THEME-013.

![Teaser](Imgs/teaser.png)</br>  
Fig.1 PKU Multi-Modality Dataset is a large-scale multi-modalities action detection dataset. This dataset contains 2 phases, phases #1 contains 51 action categories, performed by 66 distinct subjects in 3 camera views.
</div>

## Abstract
PKU-MMD is a new large scale benchmark for continuous multi-modality 3D human action understanding and covers a wide range of complex human activities with well annotated information. PKU-MMD contains 1076 long video sequences in 51 action categories, performed by 66 subjects in three camera views. It contains almost 20,000 action instances and 5.4 million frames in total. Our dataset also provides multi-modality data sources, including RGB, depth, Infrared Radiation and Skeleton. 

# Cite
```
@article{liu2017pku, 
  title={PKU-MMD: A Large Scale Benchmark for Continuous Multi-Modal Human Action Understanding},
  author={Chunhui, Liu and Yueyu, Hu and Yanghao, Li and Sijie, Song and Jiaying, Liu},
  journal={ACM Multimedia workshop},
  year={2017}
}
```

## Resources

**Paper**: [ACM Multimedia workshop](https://arxiv.org/abs/1703.07475)</br>
<!-- **Data**: [Google Drive](https://drive.google.com/drive/folders/0B20a4UzO-OyMUVpHaWdGMFY1VDQ?usp=sharing)</br> -->
**Code**: [Evaluation protocol](https://github.com/ECHO960/PKU-MMD) </br>
**Project Webpage**: http://39.96.165.147/Projects/PKUMMD/PKU-MMD.html 



## Dataset Description
PKU-MMD is our new large-scale dataset focusing on long continuous sequences action detection and multi-modality action analysis. The dataset is captured via the Kinect v2 sensor.

**Phase #1** contains 1076 long video sequences in 51 action categories, performed by 66 subjects in three camera views. It contains almost 20,000 action instances and 5.4 million frames in total. Each video lasts about 3~4 minutes (recording ratio set to 30 FPS) and contains approximately 20 action instances. The total scale of our dataset is 5,312,580 frames of 3,000 minutes with 21,545 temporally localized actions.
We choose 51 action classes in total, which are divided into two parts: 41 daily actions (drinking, waving hand, putting on the glassed, _etc._) and 10 interaction actions (hugging, shaking hands, _etc._). 66 distinct subjects are invited for our data collection. Each subjects takes part in 4 daily action videos and 2 interactive action videos.our videos only contain one part of the actions, either daily actions or interaction actions. We design 54 sequences and divide subjects into 9 groups, and each groups randomly choose 6 sequences to perform.

We provide 5 categories of resources: depth maps, RGB images, skeleton joints, infrared sequences, and RGB videos.
*   Depth maps are sequences of two dimensional depth values in millimeters. The resolution is 512x424.
*   Joint information consists of 3-dimensional locations of 25 major body joints for detected and tracked human bodies in the scene. We further provide the confidence of each joints point as appendix.
*   RGB videos are recorded in the provided resolution of 1920x1080.
*   Infrared sequences are also collected and stored frame by frame in 512x424.

## Data Format

*   Video Files:  RGB files are compressed to avi videos in 30 FPS using ffmpeg. File name format is **XXXX-V.avi** for No. **XXXX** video file in view **V**. For example **0001-L.avi** is the first video in left-sidee view.
*   Skeleton Files:  For each video, there exists a skeleton file **XXXX-V.skeleton** which contains several lines for frame-level skeleton data. Each line contains **3x25x2** float numbers for 3-dimensional locations of 25 major body joints of 2 subjects.
*   Label Files:  For each video, there exists a label file named **XXXX-V.label** illustrating the ground truth labels. Several lines will be given, each line contains 4 integers for **Label, start, end, confidence** respectively. Note that **confidence** is either **1** or **2** for slight and strong recommendation respectively.
*   Depth Files:  A folder is provided for each video which contains several images corresponding to each frame. Each image is in two-dimensional **512x424** png format.
*   RGB Files:  A folder is provided for each video which contains several images corresponding to each frame. Each image is in three-dimensional **1920x1080** jpeg format.
*   Infrared Files: A folder is provided for each video which contains several images corresponding to each frame. Each image is in one-dimensional **512x424** png format.


## More Samples

<div align=center>
 
![Teaser](Imgs/overview.png)

Fig.2 From top to bottom, these four rows show RGB, depth, skeleton and IR modalities, respectively.

</div>


<div align=center>
 
![Teaser](Imgs/samples.png)

Fig.3 We collect 51 actions performed by 66 subjects, including actions for single and pairs.

</div>

Last update: Oct 2017
