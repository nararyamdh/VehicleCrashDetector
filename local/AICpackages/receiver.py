import cv2 as cv
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from PIL import Image
import torch
import numpy as np

class Detector:
    def __init__(self):
        self.processor = AutoImageProcessor.from_pretrained("hilmantm/detr-traffic-accident-detection")
        self.model = AutoModelForObjectDetection.from_pretrained("hilmantm/detr-traffic-accident-detection")
    
    def detect(self, image):
        labels, location, scores = [], [], []

        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            labels.append(self.model.config.id2label[label.item()])
            location.append([round(i, 2) for i in box.tolist()])
            scores.append(round(score.item(), 3))
        
        return labels, location, scores