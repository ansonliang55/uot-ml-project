"""
Written by: Anson Liang

This is a handler for superpixels
"""
import numpy as np
from skimage.segmentation import mark_boundaries
from skimage.feature import hog
import matplotlib.pyplot as plt
from skimage import exposure
# @input 
#      superpixels: 2D array nxm pixels label 
# @output
#      locations: 2D array nx2 centroid locaiton of all superpixels
def getSuperPixelLocations(superpixels):
        locations = []
        numSuperpixels = np.max(superpixels)+1
        for i in xrange(0,numSuperpixels):
                indices = np.where(superpixels == i)
                x = np.mean(indices[0])
                y = np.mean(indices[1])
                locations.append([x,y])
        return np.array(locations)

# @input 
#      superpixels: 2D array nxm pixels label 
#      image: 3D array nxmx3 pixels color original image
# @output
#      color: 2D array nx3 mean color of all superpixels
def getSuperPixelMeanColor(superpixels, image):
        colors = []
        #newIm = image
        numSuperpixels = np.max(superpixels)+1
        for i in xrange(0,numSuperpixels):
                indices = np.where(superpixels==i)
                color = image[indices]
                r=np.mean(color.T[0])
                g=np.mean(color.T[1])
                b=np.mean(color.T[2])
                #newIm[indices] = [r,g,b]
                colors.append([r,g,b])
        #showPlots(newIm, numSuperpixels, superpixels)
        return np.array(colors)
# @input 
#      superpixels: 2D array nxm pixels label 
#      image: 3D array nxmx3 pixels color original image
# @output
#      color: 64D array color histogram of all superpixels
def getSuperPixelColorHistogram(superpixels, image):
        colors = []
        #newIm = image
        numSuperpixels = np.max(superpixels)+1
        for i in xrange(0,numSuperpixels):
                temp = np.zeros((1,64),dtype = int)
                indices = np.where(superpixels==i)
                color = image[indices]
                for j in xrange(0,color.shape[0]):
                    r = np.int_(color[j][0]/0.25)
                    g = np.int_(color[j][1]/0.25)
                    b = np.int_(color[j][2]/0.25)
                    if r ==4:
                        r = 3
                    if g == 4:
                        g = 3
                    if b == 4:
                        b = 3
                    x = 16*r+4*g+b*1
                    temp[0][x] = temp[0][x] + 1
                colors.append(temp[0])
        #showPlots(newIm, numSuperpixels, superpixels)

        return np.array(colors)
# @input 
#      superpixels: 2D array nxm pixels label 
#      label_image: 3D array nxm pixels color original image
#      thres: ratio threshold (0-1) for setting a superpixel to be true
# @output
#      gradient: histogram of oriented gradient
def getSuperPixelOrientedHistogram(superpixels,image):
       gradients = []
       numSuperpixels = np.max(superpixels)+1
       fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualise=True)
       print fd.shape
       print hog_image.shape
       hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))
       for i in xrange(0,numSuperpixels):
                temp = np.zeros((1,5),dtype = int)
                indices = np.where(superpixels==i)
                gradient = hog_image_rescaled[indices]
                for j in xrange(0, gradient.shape[0]):
                    x = np.int_(gradient[j] / 0.2)
                    if x == 5:
                        x = 4
                    temp[0][x] = temp[0][x] + 1
                gradients.append(temp[0])

        #showPlots(newIm, numSuperpixels, superpixels)

       return np.array(gradients)

# @input 
#      superpixels: 2D array nxm pixels label 
#      label_image: 3D array nxm pixels color original image
#      thres: ratio threshold (0-1) for setting a superpixel to be true
# @output
#      superpixel_labels: 1D Array label for super pixel (only 1 or 0)
def getSuperPixelLabel(superpixels, label_image, thres):
        #newIm = image
        superpixel_labels = []
        numSuperpixels = np.max(superpixels)+1
        labelValue = label_image.max()
        label_pixels = (label_image == labelValue)
        for i in xrange(0,numSuperpixels):
                indices = np.where(superpixels==i)
                cor_label = label_pixels[indices]
                portion_true = 1.0*np.sum(cor_label)/len(cor_label)
                if portion_true > thres:
                        superpixel_labels.append(1)
                        #newIm[indices] = [1,1,1]
                else:
                        superpixel_labels.append(0)
                        #newIm[indices] = [0,0,0]
        #showPlots(newIm, numSuperpixels, superpixels)
        # show sample test mean image
        return np.array(superpixel_labels)

# @input 
#      superpixels: 2D array nxm pixels label 
#      label_image: 3D array nxm pixels color original image
# @output
#      superpixel_labels: 1D Array label for super pixel (between 0-1)
def getSuperPixelLabelPercent(superpixels, label_image):
        #newIm = image
        superpixel_labels = []
        numSuperpixels = np.max(superpixels)+1
        labelValue = label_image.max()
        label_pixels = (label_image == labelValue)
        for i in xrange(0,numSuperpixels):
                indices = np.where(superpixels==i)
                cor_label = label_pixels[indices]
                portion_true = 1.0*np.sum(cor_label)/len(cor_label)
                superpixel_labels.append(portion_true)
        #showPlots(newIm, numSuperpixels, superpixels)
        #show sample test mean image
        return np.array(superpixel_labels)

# @input 
#      superpixels: 2D array nxm pixels label 
# @output
#      superpixel_size: 1D array number of pixels per superpixels
def getSuperPixelSize(superpixels):
        superpixel_size = []
        numSuperpixels = np.max(superpixels)+1
        for i in xrange(0,numSuperpixels):
                size = np.sum(superpixels==i)
                superpixel_size.append(size)
        return np.array(superpixel_size)


# @input 
#      superpixels: 2D array nxm pixels label 
#      image: 3D array nxmx3 pixels color original image
#      numSuperpixels: number of superpixels in superpixels
# @output (visualize data)
#      just display the image with marked superpixel boundary
def showPlots(image, numSuperpixels, superpixels):
        # show sample test mean image
        fig = plt.figure("Superpixels -- %d im_sp" % (numSuperpixels))
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(mark_boundaries(image, superpixels))
        plt.axis("off")
        plt.show()

# @input 
#      clf: classficiation object containing trained parameters
#      superpixels: 2D array nxm pixels label 
#      test_data: 2D array nxm, n data, m features
#      image: 2D array nxm original image
# @output
#      display output image indicating road
def showPrediction(clf, superpixels, test_data, image):
        newIm = image
        numSuperpixels = np.max(superpixels)+1
        for i in xrange(0,numSuperpixels):
                indices = np.where(superpixels==i)
                prediction = clf.predict_proba([test_data[i]])[0][1]
                #if prediction == 1:
                newIm[indices] = [prediction,prediction,prediction]
                #else:
                #       newIm[indices] = [0,0,0]
        showPlots(newIm, numSuperpixels, superpixels)
def showColorHistogram(colorHistogram):
        n_groups = 64
        fig, ax = plt.subplots()  
        index = np.arange(n_groups)  
        bar_width = 0.05    
        opacity = 0.2  
        histogram = plt.bar(index, colorHistogram, bar_width,alpha=opacity, color='b') 
        plt.legend()  
        plt.tight_layout()  
        plt.show()   
