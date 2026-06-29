import cv2


def addinvisiblewatermark(input_video, output_video, watermark_image, alpha=0.5):
    # Ouvrir la vidéo d'entrée
    video = cv2.VideoCapture(input_video)

    # Charger l'image du watermark avec transparence alpha
    watermark = cv2.imread(watermark_image, cv2.IMREAD_UNCHANGED)

    # Obtenir les dimensions de la vidéo
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Redimensionner le watermark pour correspondre à la taille de la vidéo
    watermark_resized = cv2.resize(watermark, (video_width, video_height))

    # Créer l'objet de sortie vidéo
    fourcc = cv2.VideoWriter_fourcc(
        *'mp4v')  # Sélectionnez le codec approprié en fonction de l'extension du fichier de sortie
    video_out = cv2.VideoWriter(output_video, fourcc, 30.0, (video_width, video_height))

    # Boucle sur les frames de la vidéo
    while True:
        # Lire le prochain frame de la vidéo
        ret, frame = video.read()

        if not ret:
            break

        # Appliquer le watermark invisible en utilisant la transparence alpha
        for i in range(3):
            frame[:, :, i] = cv2.addWeighted(frame[:, :, i], 1 - alpha, watermark_resized[:, :, i], alpha, 0)

        # Écrire le frame modifié dans la vidéo de sortie
        video_out.write(frame)

    # Libérer les ressources
    video.release()
    video_out.release()


# Exemple d'utilisation
input_video = 'C:/Users/DELL/Desktop/videoprojet/video/video1.mp4'
output_video = 'C:/Users/DELL/Desktop/videoprojet/video/watermark5.mp4'
watermark_image = 'C:/Users/DELL/Desktop/videoprojet/video/TATTOO.png'
alpha = 0.1

addinvisiblewatermark(input_video, output_video, watermark_image, alpha)







