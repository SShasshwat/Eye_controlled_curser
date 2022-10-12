import cv2    #for image processing
import mediapipe as mp
import pyautogui
cam = cv2.VideoCapture(0)    # fisrt video capturing device
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()       #screen width and height
while True:
    _, frame = cam.read()   # to read every frame of video
    frame = cv2.flip(frame, 1)      # to flip the frame vertically
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):      # landmark points of eye
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))       # green colour circle
            if id == 1:     # picking out one point from those 5 points
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)        # to move pointer
        left = [landmarks[145], landmarks[159]]     # uppper and lower landmark of left eye
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))     # yellow colour circle
            # print(left[0].y - left[1].y)      # to check the difference between two eye point
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
    cv2.imshow('Eye Controlled Mouse', frame)       # to show some image im stand for image and show
    cv2.waitKey(1)