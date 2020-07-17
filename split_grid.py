# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:51:01 2020

@author: anjit
"""
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def digitize_captured(sudo):
    """
    Arguments:
    sudo -- A squared and unsolved sudoku image
    my_model -- A classification CNN model trained on 10 classes
                classes: blank images, 1, 2, .., 9

    Returns:
    grid -- a (9 x 9) matrix of all predicted digits
    """

    delta_w, delta_h = int(sudo.shape[0] / 9), int(sudo.shape[1] / 9)   # Ratios to divide the image by
    #resizes = []                  # an empty list where we will append the cropped cells
    dd = 6
    for h in range(9):
        for w in range(9):
            crop = sudo[(h*delta_w+dd):((h+1)*delta_w-dd),(w*delta_h+dd):((w+1)*delta_h-dd)]        # extract a cell to predict its class
            #cv2.imshow('crop',crop)	
            cv2.imwrite(str(h) + str(w) + '.png',crop)

def image_ocr(image):
    image = cv2.imread(image)
    return_string = pytesseract.image_to_string(image, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return return_string


def sudoku_grid():
    ocr_string = lambda s: 0 if s == "" else int(s)
    board=[]
    for i in range (0,9):
           board.append([])
           for j in range(0,9):
               board[i].append(0)
    for h in range(9):
        for w in range(9):
            board[h][w]= ocr_string(image_ocr(str(h) + str(w) + '.png'))
            print(h,w, board[h][w])
    return board


