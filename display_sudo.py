# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 09:43:40 2020

@author: anjit
"""

import cv2


def displaySolution(image, final):
    
    """Function that allows to overlay the sudoku solution to a blank grid """
    image = image.copy()
    cell_width = image.shape[1] //9
    cell_height = image.shape[0] // 9
    print(cell_height, cell_width)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(9):
        for j in range(9):
            text = str(final[i][j])
            offsetx = cell_width // 15
            offsety = cell_height //15
            (text_height, text_width), baseline = cv2.getTextSize(text,font, fontScale = 1, thickness = 3)
            bottomleft = cell_width*j +(cell_width - text_width) // 2 + offsetx
            bottomright = cell_height*(i+1) -(cell_height - text_height) // 2 + offsety
            image = cv2.putText(image, text, (int(bottomleft), int(bottomright)), font, 1, (255,0,0), thickness = 3, lineType = cv2.LINE_AA)
    
    return image

def print_sudo(sudo_grid):
    
    """
    The function that helps in printing the sudoku grid in the console in a better arrangement
    """
    for i in range(len(sudo_grid)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudo_grid[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(sudo_grid[i][j]) + " "
        print(line)