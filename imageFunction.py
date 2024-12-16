import cv2
import numpy as np

def imageProcess(arquivo):
    imagem = cv2.imread(arquivo)
    h, w, _ = np.shape(imagem)
    print(f"Tamanho - H:{h}, W: {w}")
    proporcao = 4
    print(f"Redimensionando Imagem - Proporção 1/{proporcao}")
    imagem= cv2.resize(imagem, (int(w/proporcao), int(h/proporcao))) 
    imagemHsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    cv2.imshow("ImagemHSV", imagemHsv)
    lowerGreen = np.array([31,42,101])
    upperGreen = np.array([130,255,255])
    
    imageMask = cv2.inRange(imagemHsv, lowerGreen, upperGreen)
    cv2.imshow("ImageMaskOriginal", imageMask)
    
    # Define o kernel para operações morfológicas
    kernel_size = 5  # Aumente ou diminua conforme necessário
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Aplica a operação de fechamento para agrupar pixels brancos próximos
    imageMask = cv2.morphologyEx(imageMask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("ImageMask", imageMask)
    contours, _ = cv2.findContours(imageMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 100  # Ajuste esse valor conforme o necessário
    aspect_ratio_min = 0.5
    aspect_ratio_max = 1.2
    for contour in contours:
        area = cv2.contourArea(contour)
        if area <= min_area and area>5: #and area>20
            # Destaca o contorno no output com uma cor específica
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0  # Evita divisão por zero
            if aspect_ratio_min <= aspect_ratio <= aspect_ratio_max:
            # Desenha um quadrado verde ao redor de contornos maiores que são aproximadamente quadrados
                cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 0, 255), 2)
            else:
                # Ignora objetos que não são aproximadamente quadrados
                continue

    # Exibir o resultado
    cv2.imshow("Img: "+str(arquivo), imagem)
    #cv2.imshow("Objetos Destacados", output)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Normaliza as cores da imagem

def normalizar_cores(arquivo, k=5):
    # Converte a imagem para float32
    
    imagem = cv2.imread(arquivo)
    h,w,bpp = np.shape(imagem)
    print(f"Tamanho - H:{h}, W: {w}")
    proporcao = 4
    print(f"Redimensionando Imagem - Proporção 1/{proporcao}")
    imagem= cv2.resize(imagem, (int(w/proporcao), int(h/proporcao))) 
    imagem_data = np.float32(imagem)
    # Redimensiona a imagem para um vetor 2D
    pixels = imagem_data.reshape((-1, 3))

    # Critério de parada para o K-means
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, k, None, criterio, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Converte os centros de volta para uint8
    centers = np.uint8(centers)
    # Mapeia cada pixel para o centro de cor mais próximo
    imagem_normalizada = centers[labels.flatten()]
    # Redimensiona de volta para o formato original da imagem
    imagem_normalizada = imagem_normalizada.reshape(imagem.shape)
    cv2.imshow("Normalizada", imagem_normalizada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return imagem_normalizada
    
def analisaCorLimiar(cor, item, limiar ):
    corB = item[0]
    corBIni = corB - limiar
    corBFim = corB + limiar
    corG = item[1]
    corGIni = corG - limiar
    corGFim = corG + limiar
    corR = item[2]
    corRIni = corR - limiar
    corRFim = corR + limiar

    if cor[0] >= corBIni and cor[0]<=corBFim:
        if cor[1] >= corGIni and cor[1]<=corGFim:
            if cor[2] >= corRIni and cor[1]<=corRFim:
                return 1
    else:
        return 0

    return 1

def analisaLimiar(lista, valor , limiar):
    retorno = True
    if len(lista) == 0:
        return True
    for item in lista:
        corB = item[0]
        corBIni = corB - limiar
        corBFim = corB + limiar
        corG = item[1]
        corGIni = corG - limiar
        corGFim = corG + limiar
        corR = item[2]
        corRIni = corR - limiar
        corRFim = corR + limiar
        if valor[0] >=corBIni and valor[0]<=corBFim:
            if corGIni<=valor[1]<=corGFim:
                if corRIni<=valor[2]<=corRFim:
                    retorno = False
    return retorno

