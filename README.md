# COMP_SCI496-SML Project - Image Retrieval

## Problem Statement

Similar to searching information in the form of text, the task of image retrieval is to find information in the form of image that convey a certain concept a user has in mind. Such concept can be expressed purely through text, a similar image, or a combination of both. A good image retrieval system can be useful in various scenarios. For example, a customer shopping for some clothes can upload an image resembling what he/she wants, and then add some potential adjustments to the uploaded image. The system will find the closest image representing the cloth he/she desires.

## Input/Output

**Input**

- An image
- An adjustment text

**Output**

- A set of retrieved images

## Core Model

The front-end demo app is built on top of [tirg](https://github.com/google/tirg), whose idea is to formulate a query representation by composing vectorized image and text information. The vectorized image features are filtered using the text information so that only relevant image information is kept, whereas the all text features are retained. This model is proven to be relatively accurate on the [CSS3D](https://drive.google.com/file/d/1wPqMw-HKmXUG2qTgYBiTNUnjz83hA2tY/view) dataset, but for more real life dataset such as [Fashion200K](https://github.com/xthan/fashion-200k), which is also used in this project, there is still room for improvement.

## Deliverables

## Running through Docker Containers

## Model Training

### Dataset Construction

### Training and Evaluation

## Reference