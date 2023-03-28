# DEEP-V
## Streamlit Interface
A streamlit interface gives the user the possibility select a city area and run the model.
The model returns the outlines and m2 of solar panels.
It also calculates the amount of wattage that potentially is produced by the panels. 

![unnamed-4](https://user-images.githubusercontent.com/34649640/228357652-b57acfd6-ee2e-4811-a181-ff1ab5f39a84.png)
![unnamed-5](https://user-images.githubusercontent.com/34649640/228357637-9c218122-a832-4c51-b711-bfcfc1784aed.png)


## FastAPI
The streamlit interface calls an fast API interface gets requests for a set of coordinates and then:
- Downloads images in tiles from a google maps API.
- Saves them on GCP.
- Runs inference on them.
- Calculates KPIs

## Trained model
It contains a trained MRCNN model trained on Solar Panels in California and China. 
Images were converted to COCO format for training the model.
The model can either be accessed locally or on GCP. 

![unnamed-2](https://user-images.githubusercontent.com/34649640/228357665-2ab8d87b-a116-4771-975e-fe636cbe070f.png)


We have developed an identification model based on a complex structure of trained algorithms that emulate the human brain neural structure i.e., deep learning. In essence, we trained a Deep Convolutional Neural Network model to localize and identify solar panels from satellite imagery by assigning pixel areas of input images to a class (within a confidence interval) i.e., semantic segmentation. The architecture used for the model is the Mask Regional Convolutional Neural Network (MRCNN), based on a ResNet-50 backbone. The neural network framework was trained on labelled images of California with a size of 256x256 pixels. The labelling of each input image was done with two-pixel coordinates that map a polygon area, containing photovoltaic installations of rooftops or residential and commercial areas. The noted area was then processed into a binary mask, which is the cornerstone of the two-step recursive training, allowing us to perform statistical inference via output segmentation masks. In order to support the convergence of learning rates during the training process, we used the Microsoft-COCO pre-trained weights as starting points for the optimization[1], which, along with GPU parallelization technology, made the training feasible in a reasonable amount of time[2]. The diagram below depicts the model process.

![unnamed-3](https://user-images.githubusercontent.com/34649640/228357658-1724f680-1a64-4cae-9b3c-e060f3143c3f.png)

After a feature map is extracted via the backbone, region proposals are generated based on reference boxes known as anchors or bounding-boxes, labels are assigned to these anchors based on an optimization process[4]. Furthermore, regions of interest are projected on the feature maps from the backbone in order to get a classification later, a bounding-box regression layer and a mask prediction layer. In a nutshell, our model performs object detection and area segmentation for classification on pixel areas of input images. 

[1] This is known as Transfer Learning and is a common practice in Deep Learning applications.
[2] In total, iterations were performed for a total of 77 epochs 
[3] The main role of the backbone is the extraction of feature maps from input images, ensuring detection of PV installations on multiple backgrounds and scales.
[4] This step leads to a box-classification and a box regression which provide a probability of a predicted region proposal being a solar panel and with predicted coordinates


For our baseline implementation, a sample of 800+ images was used, with respective random test and validation subsamples that helped  avoiding overfitting. After fine tuning and evaluating the model performance on precision, recall and a validation loss function, our model was able to accurately detect the location and shape of PV installations, with an out-of-sample performance of almost 90% accuracy[1], leading to robust inference on satellite rooftop imagery from China, Switzerland and The Netherlands. Below some images that illustrate the out-of-sample performance of the model across geographies. 

Deep-PV model approach has the notable advantage that an extent and granular configuration of parameters is possible, which allows specific-scenario and tailored solutions for endless commercial applications. Moreover, rooftop satellite images present multiple challenges for the learning and identification process (see below). Thus, it is necessary to keep working on the strength of the model by training on a larger set of imagery across countries, particularly for avoiding false positive regions. Further development on this methodology is needed in order to enhance its precision and extend its scope to different geographies and rooftop configurations.


