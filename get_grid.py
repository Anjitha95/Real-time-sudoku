# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:47:58 2020

@author: anjit
"""
import cv2
import numpy as np


def preprocess(image):
    
    
    """ This is a function that converts the image to gray scale and
        performs guassian blur to remove the noice and apply adaptive 
        threshold"""
        
    # Convert to grayscale image 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Guassian Blur to reduce Nocie
    blur_image = cv2.GaussianBlur(gray_image, (5,5), 0)
    
    # Apply thresh hold
    thresh = cv2.adaptiveThreshold(blur_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)
    
    return thresh
        
def get_grid_loc(image, height, width):
        """
        Expects preprocessed binary image
        """

        grid_loc = None
        
        detected = False # flag value that checks if sudoku is detected or not

        # maybe better than adaptive thresholding
        # edge = cv2.Canny(image, 50, 150, apertureSize=3)

        # invert black/white so that contours are white
        invert = cv2.bitwise_not(image)

        hough_lines = get_hough_lines(invert, height, width)

        if hough_lines is not None:
            grid_loc = get_max_rect(hough_lines)

            # DEBUG : draw max rectangle -------------------
        if grid_loc is not None:
            cv2.imshow('Max Area Rectangle', cv2.polylines(
            cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), [np.int32(grid_loc)], True, (0, 255, 0), 2))
            # ----------------------------------------------
        if grid_loc is None:
            return [], detected
        else: 
            return grid_loc, True

def get_hough_lines(image, height, width):

    hough_lines = None

    # get hough transform
    lines = cv2.HoughLinesP(image, 1, np.pi/180, 50, minLineLength=50, maxLineGap=5)

    # check if any lines were found
    if (lines is not None) and (len(lines) != 0):
        # create blank black image with only one color channel (don't use UMat, overhead too big for simple draw)
        hough_lines = np.zeros((height, width), dtype=np.uint8)

        # draw all found lines in source image
        for line in lines:
            x_1, y_1, x_2, y_2 = line[0]
            # draw white line
            cv2.line(hough_lines, (x_1, y_1), (x_2, y_2), (255, 255, 255), 2)

        # DEBUG ---------------
    #cv2.imshow("hough lines", hough_lines)
            # ---------------------

    return hough_lines
    
def get_max_rect(image):
    
    max_rectangle = None

    # get all contours in given image (contours must be white)
    contours, _ = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # atleast one contour must be found
    if len(contours) > 0:

        max_contour = None

        for contour in contours:
            # threshold for contour area
            if cv2.contourArea(contour) < (image.shape[0] * image.shape[1]) / 20:
                break

            # approximate polygon of given contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            poly_approx = cv2.approxPolyDP(contour, epsilon, True)

            # rectangle needs only 4 points
            if len(poly_approx) == 4:
                max_contour = poly_approx
                break

        if max_contour is not None:

            max_rectangle = np.zeros((4, 2), dtype=np.float32)

            # reshape for convenience
            points = max_contour.reshape(-1, 2)

            # the top-left point has the smallest sum
            # whereas the bottom-right has the largest sum
            sum_of = points.sum(axis=1)
            max_rectangle[0] = points[np.argmin(sum_of)]
            max_rectangle[2] = points[np.argmax(sum_of)]

            # compute the difference between the points -- the top-right
            # will have the minumum difference and the bottom-left will
            # have the maximum difference
            diff_of = np.diff(points, axis=1)
            max_rectangle[1] = points[np.argmin(diff_of)]
            max_rectangle[3] = points[np.argmax(diff_of)]

    return max_rectangle 

# perspective if you look direcly from above


def transform_image_perspective(image, current_perspective):
    
    transform_matrix = None
    grid_image_shape = None
    goal_perspective = None
    grid_image_width = 450
    grid_image_height = 450
    grid_image_shape = (grid_image_width, grid_image_height)
    goal_perspective = np.array([[0, 0], [grid_image_width, 0],
                                  [grid_image_width, grid_image_height], [0, grid_image_height]], dtype=np.float32)
    # get inverse transformation of current prespectiv and apply it on given image
    transform_matrix = cv2.getPerspectiveTransform(current_perspective, goal_perspective)
    wrap = cv2.warpPerspective(image, transform_matrix, grid_image_shape)
    
    return wrap, transform_matrix 

def inverse_transform_image_perspective(self, image, full_image_height, full_image_width):
    assert self.transform_matrix is not None
    return cv2.warpPerspective(image, self.transform_matrix, (full_image_width, full_image_height), flags=cv2.WARP_INVERSE_MAP)
