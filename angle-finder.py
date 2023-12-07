import cv2
import math

def calculate_angle(center, point1, point2):
    vector1 = (point1[0] - center[0], point1[1] - center[1])
    vector2 = (point2[0] - center[0], point2[1] - center[1])

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    cosine_theta = dot_product / (magnitude1 * magnitude2)
    angle_radians = math.acos(cosine_theta)
    angle_degrees = math.degrees(angle_radians)

    return round(angle_degrees)

def draw_lines(image, center, point1, point2):
    cv2.line(image, center, point1, (0, 0, 255), 2)
    cv2.line(image, center, point2, (0, 0, 255), 2)

def reset_image(image_path, points):
    img = cv2.imread(image_path)
    for point in points:
        cv2.circle(img, tuple(point), 5, (0, 0, 255), -1)
    return img

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(params['points']) < 3:
            params['points'].append((x, y))

            if len(params['points']) == 1:
                params['center'] = (x, y)
            elif len(params['points']) == 2 or len(params['points']) == 3:
                draw_lines(params['image'], params['center'], params['points'][1], params['points'][-1])

            cv2.circle(params['image'], (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('Image', params['image'])

            if len(params['points']) == 3:
                angle = calculate_angle(params['center'], params['points'][1], params['points'][2])
                cv2.putText(params['image'], f"Angle: {int(angle)} derece", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Image', params['image'])

    if cv2.waitKey(2) & 0xFF == ord("d"):
        params["points"] = []
        params['image'] = reset_image(params['image_path'], params["points"])
        cv2.imshow('Image', params['image'])

if __name__ == "__main__":
    image_path = "image.png"  # File path of picture
    image = cv2.imread(image_path)

    if image is not None:
        cv2.imshow('Image', image)
        points = []
        center = (0, 0)  # The first dot is the center.
        cv2.setMouseCallback('Image', click_event, {'image': image, 'points': points, 'center': center, 'image_path': image_path})

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # exit when press ESC
                break


        cv2.destroyAllWindows()
    else:
        print("The picture cannot load.")
