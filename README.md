# Find my pic
Elbrus Bootcamp | Phase-3 | Team project


## 🦸‍♂️Team
1. [Viktoriia Ivanova](https://github.com/Vikaska031)
2. [Vladimir Kadnikov](https://github.com/vkadnikov92)

## 🎯 Objectives
Develop a service where the user enters a text query, and they receive 5 images that best match this description.

## 📐 Model
The Contrastive Language-Image Pre-Training (CLIP) module has been utilized.

## 📚 Library 

```typescript

import streamlit as st
from PIL import Image
import pandas as pd
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
import os
import zipfile
```
	price

## 🧠 Releases

Release 1.0 🦄

In this release, the service takes a user query in a text field and returns 5 random images from the 'img' folder (52 photos) along with user-provided image descriptions.

Release 2.0✨

A 'main.py' script has been implemented in this release. It accepts a text query, vectorizes it, and returns the 5 most similar images based on a similarity metric.
A 'get_similarity.py' script has been implemented, containing the function for finding the 5 images closest to the text query.

Release 3.0🎉

Added the capability to generate descriptions for uploaded images.

## How to use this?
Simply click the [link](https://huggingface.co/spaces/Vladimirktan/find-my-pic-app)  and enjoy the experience.
