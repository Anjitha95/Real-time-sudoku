# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:33:10 2020

@author: anjitha
"""
# Import all standard libraries and class
import cv2
#import numpy as np
import solve_sudoku
import get_grid
import pytesseract
import split_grid
import display_sudo

# If path not set change the path given below to the path where your tesseract.exe file exists
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


           
stream = cv2.VideoCapture(0)

if not stream.isOpened():
    stream.release()
    print("Error while opening the camera")

SUDOKU_GRID_HEIGHT = 450
SUDOKU_GRID_WIDTH = 450
stream_width = int(stream.get(3))
stream_height = int(stream.get(4))
font = cv2.FONT_HERSHEY_SIMPLEX
message = "Sudoku Not detected"


while(True):
    
    ret, frame = stream.read()
    
    blank_grid = cv2.imread('blank_grid.png')
    
    preprocessed_frame = get_grid.preprocess(frame)
    
    grid_loc, detected = get_grid.get_grid_loc(preprocessed_frame, stream_height, stream_width)
    
    if detected:
        sudoku_grid_image, matrix = get_grid.transform_image_perspective(preprocessed_frame, grid_loc)
         # show converted frame
        #cv2.imshow("Perspective Transformed", sudoku_grid_image)
        message = "Sudoku Detected"
        cv2.imwrite('Sudoku.png',sudoku_grid_image)
        split_grid.digitize_captured(sudoku_grid_image)
        """sudoku_grid = split_grid.sudoku_grid()
        print("sudoku before solving")
        print("\n\n")
        display_sudo.print_sudo(sudoku_grid)
        solve_sudoku.solve(sudoku_grid)
        print("sudoku after solving")
        print("\n\n")
        display_sudo.print_sudo(sudoku_grid)
        solution = display_sudo.displaySolution(blank_grid, sudoku_grid)
        cv2.imshow("Result", solution)"""
    #cv2.imshow("Thresh", preprocessed_frame)
    
    #cv2.putText(frame, message, (10, 350), font, 0.6, (255, 0, 0))
    cv2.imshow("Sudoku Frame", frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
            print("You Quit from the game")
            break

stream.release()
cv2.destroyAllWindows()

