# DEEP-V
## Streamlit Interface
A streamlit interface gives the user the possibility select a city area and run the model.
The model returns the outlines and m2 of solar panels.
It also calculates the amount of wattage that potentially is produced by the panels. 

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

*** This documentation is very incomplete and part of a rushed project ***
