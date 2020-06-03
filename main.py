#!/usr/bin/env python3
import PIL
from PIL import Image
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import numpy as np
import os
import sys
from voronoi import Voronoi, Polygon


class VoronoiGraph():
    """
    This class encapsulates all stuff related to voronoi diagram
    """

    def __init__(self):
        pass

    def _loadMap(self):
        """
        Load image png and converst to list of tuples (map) including only obstacles
        ---
        Map is stored inside self.map
        """
        
        #image = Image.open("map_voronoi.png") # takes way to much to compute which is another drawback (723x446)
        image = Image.open("map_voronoi_big.png")

        bw = image.convert('L')
        # bw.show()
        map = np.asarray(bw.copy())
        self._convertToMap(map)

    def _convertToMap(self, n_array):
        """
        convert array to obstacles map including points where obstacles are
        """
        cnt_x = 0
        cnt_y = 0
        m = []
        for i in n_array:
            cnt_x += 1
            cnt_y = 0
            for j in i:
                cnt_y += 1
                if(j != 255):
                    m.append([cnt_x, cnt_y])

        self.map = m


    def dist2(self, p1, p2):
        return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

    def fuse(self, points, d):
        ret = []
        d2 = d * d
        n = len(points)
        taken = [False] * n
        for i in range(n):
            if not taken[i]:
                count = 1
                point = [points[i][0], points[i][1]]
                taken[i] = True
                for j in range(i+1, n):
                    if self.dist2(points[i], points[j]) < d2:
                        point[0] += points[j][0]
                        point[1] += points[j][1]
                        count += 1
                        taken[j] = True
                point[0] /= count
                point[1] /= count
                ret.append((point[0], point[1]))
        return ret

    def _custom_round(self, x, base=5):
        return int(base * round(float(x)/base))

    def _addPoint(self, lst, p_x, p_y):
        """
        Adds 4 points close to wanted point
        """
        lst.append([p_x-1, p_y-1])
        lst.append([p_x+1, p_y-1])
        lst.append([p_x-1, p_y+1])
        lst.append([p_x+1, p_y+1])
        return lst

    def testVoronoi(self):
        """
        I ve tested how voronoi package works but it has problems when dataset of points is greater than 20
        """
        print("test using voronoi lib")
        
        self._loadMap()
        # print("len self map:", len(self.map))
        print(self.map)
        raw_points = self.map
        points = self.fuse(raw_points.copy(), 6) # here is magic of rounding problem is that i have to specify round radius (2nd param) by my self

        # Define a bounding box
        polygon = Polygon([
            (0.0, 0.0),
            (0.0, 400.0),
            (400.0, 0.0),
            (400.0, 400.0)
        ])

        # Initialize the algorithm
        v = Voronoi(polygon)

        # Create the diagram
        v.create_diagram(points=points, vis_steps=False,
                         verbose=False, vis_result=True, vis_tree=True)

        # Get properties
        edges = v.edges
        vertices = v.vertices
        arcs = v.arcs
        points = v.points
        print("voronoi properties:")
        print("edges:", edges)
        print("vertices:", vertices)
        print("arcs:", arcs)
        print("points:", points)
        print(v.points[0].get_coordinates())
        for point in v.points:
            print(f"{(point.x, point.y)} \t {point.cell_size()}")


if __name__ == "__main__":
    v = VoronoiGraph()
    v.testVoronoi()