import cv2
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
from ultralytics import YOLO
from PIL import Image
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import os

# Load YOLO model once at the start
model = YOLO('yolov8n.pt')

# Path to save the output image
OUTPUT_IMAGE_PATH = "output_image.jpg"

@csrf_exempt
def detect_people(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            image = Image.open(image_file)

            # Convert image to a format YOLO can process
            image_array = np.array(image)

            # Run detection
            results = model(image_array)

            # Filter results for 'person' class (class ID 0 in COCO dataset)
            person_count = sum(1 for r in results[0].boxes.data if int(r[-1]) == 0)

            # Draw bounding boxes on the image
            annotated_image = results[0].plot()  # Render the results with bounding boxes

            # Save the output image
            cv2.imwrite(OUTPUT_IMAGE_PATH, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

            # Serve the output image and person count
            return JsonResponse({'person_count': person_count, 'output_image': f'/static/{OUTPUT_IMAGE_PATH}'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def video_stream():
    # Open webcam or video file
    video_capture = cv2.VideoCapture(0)  # Use 0 for webcam, or replace with video file path

    while True:
        # Read a frame from the video
        ret, frame = video_capture.read()
        if not ret:
            break

        # Process the frame with YOLO
        results = model(frame)

        # Draw bounding boxes on the frame
        annotated_frame = results[0].plot()

        # Count people (class ID 0 in COCO dataset)
        person_count = sum(1 for r in results[0].boxes.data if int(r[-1]) == 0)

        # Overlay the person count on the frame
        cv2.putText(annotated_frame, f"People Count: {person_count}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Encode the frame as JPEG
        _, jpeg_frame = cv2.imencode('.jpg', annotated_frame)

        # Yield the encoded frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame.tobytes() + b'\r\n')

    video_capture.release()

# Django view to serve the video feed
def detect_people_video(request):
    return StreamingHttpResponse(video_stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')