import cv2

def draw(img, location, score, label):
    x = cv2.rectangle(img,(location[0],location[1]), (location[2],location[3]), (0, 0, 255), 3)
    x = cv2.putText(x, f"{label}: {score:.2f}",(location[0],location[1]-20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0, 0, 255),2)
    return x