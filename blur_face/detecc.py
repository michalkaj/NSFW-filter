import glob
import os
import torch
from PIL import Image, ImageDraw
from facenet_pytorch import MTCNN, InceptionResnetV1
from facenet_pytorch.models.utils.detect_face import extract_face

workers = 0 if os.name == 'nt' else 4
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True, device=device, keep_all=True)

resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
counter = 0

for file in glob.glob("test_imgs/*.*"):
    img = Image.open(file).convert('RGB')
    boxes, probs, points = mtcnn.detect(img, landmarks=True)
    img_draw = img.copy()
    draw = ImageDraw.Draw(img_draw)
    print(str(file) + " " + str(boxes))
    if boxes is not None:
        for i, (box, point) in enumerate(zip(boxes, points)):
            draw.rectangle(box.tolist(), width=5)
            for p in point:
                draw.rectangle((p-10).tolist() + (p+10).tolist(), width=10)
            extract_face(img, box)
        img_draw.save('saved/annotated_faces_{}.png'.format(counter))
        counter += 1
