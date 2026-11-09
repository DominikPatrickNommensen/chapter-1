import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 

import numpy as np
import pandas as pd
import geopandas as gpd

from shapely.ops import nearest_points
from shapely import MultiPolygon, Point, MultiLineString, LineString, intersection
import matplotlib.pyplot as plt


class Yjunction:
    '''
    Class for representing and analyzing Y-junctions.

    Attributes:
        point (Point): The intersection point of the Y-junction.
        lines (GeoSeries): A GeoSeries of LineString objects representing the lines connecting at the Y-junction.
        intersects_around_point_dict (dict): A dictionary storing intersection points for various radii.
        radii (list): A list of radii used for calculations.
        radius_point_angle_dict (dict): A dictionary storing angles for intersection points for various radii.
        radius_points_anglebetween_dict (dict): A dictionary storing angles between points for each radius.
        center_radius_opening_direction (dict): A dictionary storing the opening angles and bisector directions for each point pair of each radius.
    '''
    
    color_list = ['blue','red','olive']
    
    def __init__(self, point, lines):
        "Sets uo the lines, intersection point and radii of and around the Y-junction"
        
        self.point = self._evaluate_point(point)
        self.lines = self._evaluate_lines(lines)
        
    def _evaluate_point(self, point):
        "Evaluates if the point is of correct type"
        if not (isinstance(point,Point)):
            raise ValueError("Point is not a Shapely Point!")
        else:
            return point
            
    def _evaluate_lines(self, lines):
        "Raises an Error if lines are not shapely LineString or returns the lines"
        try:
            if not lines.apply(lambda x: isinstance(x, LineString)).all():
                raise ValueError("One or more lines in lines are not of type Shapely LineString!")
            else:
                return lines
        except AttributeError as e:
            raise AttributeError("Your lines are not stored as a GeoSeries!") from e
            
    def _evaluate_radius(self, radius):
        "Returns True if radius is single value, False if list or raises an Error"
        if isinstance(radius, (int, float)):
            return True
        elif isinstance(radius, list):
            return False
        else:
            raise ValueError("Radius is not numeric and not a list!")

    def _setup_radii(self, radius):
        "Returns a sorted list of radii"
        singleradius = self._evaluate_radius(radius)
        maxradius = self._get_max_radius()
        radii = self._populate_radii(radius, maxradius, singleradius)
        return sorted(radii)
            
    def _get_buffer_around_point(self, radius):
        "Returns the buffer around a point as Polygon" 
        return self.point.buffer(radius)

    def _farthest_distance_to_line(self, line):
        "Returns the point along a line that is the furthest away from point"
        return np.max([self.point.distance(Point(coord)) for coord in line.coords])
        
    def _get_max_radius(self):
        "Returns the maximum radius around the point that instersects with all lines"
        farthest_points_on_lines = []
        for line in self.lines:
            farthest_points_on_lines.append(self._farthest_distance_to_line(line))
        return np.min(farthest_points_on_lines)
        
    def _compare_radii(self, radius, maxradius):
        "Returns the valid radius"
        if not (radius <= 0):
            if maxradius < radius:
                return maxradius
            else:
                return radius
        else:
            raise ValueError("One or more radii are negative!")
            
    def _populate_radii(self, radius, maxradius, singleradius):
        "Return a list of valid radii"
        radii = []
        # radiussteps = np.array([0.01, 0.25, 0.5, 0.75, 1]) # 1%, 25%, 50%, 75%, 100%
        radiussteps = np.array([0.05, 0.25, 0.5, 0.75, 0.95]) # 5%, 25%, 50%, 75%, 95%
        
        if singleradius:
            radii.append(self._compare_radii(radius, maxradius))
        else:
            if len(radius) == 1:
                radiusvalid = self._compare_radii(radius[-1], maxradius)
                for radnorm in (radiussteps * radiusvalid):
                    radii.append(radnorm)
            else:
                for raddiscrete in radius:
                    raddiscretevalid = self._compare_radii(raddiscrete, maxradius)
                    if not raddiscretevalid in radii:
                        radii.append(raddiscretevalid)
        return radii

    def get_radius_intersects(self, radius=0.051):
        "Takes a radius as number, list or a list of radii and returns the points of intersection with junction lines"
        self.intersects_around_point_dict = {}
        self.radii = self._setup_radii(radius)
        for rad in self.radii:
            self.intersects_around_point_dict[str(rad)] = self._fill_intersects_around_point_dict(rad)
        return self.intersects_around_point_dict

    def get_angle_intersects(self):
        "Calculates the angles for all radii line intersections and stores them in a dict"
        self.radius_point_angle_dict = {}
        for rad, pnts in self.intersects_around_point_dict.items():
            self.radius_point_angle_dict[rad] = self._calculate_angle_of_points_and_sort(pnts)
        return self.radius_point_angle_dict

    def _orientate_line(self, line, point):
        if point.equals(Point(line.coords[0])):
            return line
        elif point.equals(Point(line.coords[-1])):
            return line.reverse()
        else:
            raise ValueError("Point is neither the start nor the end of the line")
            
    def _nearest_point_along_line(self, line, multipoint):
        nearest_point = None
        min_distance = float('inf')
        templine = self._orientate_line(line, self.point)
        for point in multipoint.geoms:
            distance = templine.project(point)
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
        return nearest_point
        
    def _fill_intersects_around_point_dict(self, radius):
        "Returns the Points along each line that intersect with the radius around the junction point"
        # TODO: double check if all this is really working the right way!
        point_buffer = self._get_buffer_around_point(radius)
        tempintersects = point_buffer.exterior.intersection(self.lines)#[~point_buffer.exterior.intersection(self.lines).is_empty]
        # print(tempintersects)
        if tempintersects.is_empty.any():
            for idx,_ in tempintersects[tempintersects.is_empty].items():
                # print(Point(self.lines[idx].coords[0]).distance(self.point))
                # print(Point(self.lines[idx].coords[1]).distance(self.point))
                templine = self._orientate_line(self.lines[idx], self.point)
                tempintersects[idx] = Point(templine.coords[-1])
        if tempintersects[(tempintersects.geom_type == 'MultiPoint')].empty:
            return tempintersects.values
        else:
            sglpnts = tempintersects[~(tempintersects.geom_type == 'MultiPoint')]
            mltpnts = tempintersects[(tempintersects.geom_type == 'MultiPoint')]
            nearestpntslist = []
            for idx, mltpnt in mltpnts.items():
                nearestpnt = self._nearest_point_along_line(self.lines[idx], mltpnt)
                nearestpntslist.append(nearestpnt)
            return pd.concat([sglpnts, gpd.GeoSeries(nearestpntslist, crs=sglpnts.crs)]).values

    def _calculate_angle_of_points_and_sort(self, points):
        "Returns the angle of a point relative to the junction point along a line that intersects with a radius around the junction point."
        temppntsangs = {}
        # print(points)
        for pnt in points:
            # print(pnt)
            # print(np.arctan2((pnt.y-self.point.y),(pnt.x-self.point.x)))
            temppntsangs[pnt] = np.arctan2((pnt.y-self.point.y),(pnt.x-self.point.x))
        # print(temppntsangs)
        return dict(sorted(temppntsangs.items(), key=lambda item: item[1]))

    def get_angle_between_points(self):
        "Get the angles between intersect points for each radii"
        self.radius_points_anglebetween_dict = {}
        for rad, pnts in self.radius_point_angle_dict.items():

            try:
                pnt1, pnt2, pnt3 = list(pnts.keys())
                remove_radius = None
            except ValueError:
                # This is crucial when two lines end it the same point and there is effectively no Y-junction anymore; remove this radius from all dicts (makes it only 4 radii in total)
                print("Radius {} for Y-junction at {} has no three unique points".format(rad, self.point))
                remove_radius = rad
                continue
                
            ang12 = self.angle_between((pnt1.x-self.point.x, pnt1.y-self.point.y),(pnt2.x-self.point.x, pnt2.y-self.point.y))
            ang23 = self.angle_between((pnt2.x-self.point.x, pnt2.y-self.point.y),(pnt3.x-self.point.x, pnt3.y-self.point.y))
            ang31 = self.angle_between((pnt3.x-self.point.x, pnt3.y-self.point.y),(pnt1.x-self.point.x, pnt1.y-self.point.y))
    
            ang12 = self.evaluate_angle_no_overlap(pnts[pnt1], pnts[pnt2], ang12)
            ang23 = self.evaluate_angle_no_overlap(pnts[pnt2], pnts[pnt3], ang23)
            ang31 = self.evaluate_angle_no_overlap(pnts[pnt3], pnts[pnt1], ang31)

            self.radius_points_anglebetween_dict[rad] = {(pnt1, pnt2) : ang12, (pnt2, pnt3) : ang23, (pnt3, pnt1) : ang31}
        
        if remove_radius is not None:
            self.radii.pop()
            del self.intersects_around_point_dict[rad]
            del self.radius_point_angle_dict[rad]
                
        return self.radius_points_anglebetween_dict
        
    def evaluate_angle_no_overlap(self, ang1, ang2, angbtw):
        "Makes sure the whole circle is used and angles between point pairs don't overlap"
        if ((ang2 - ang1) < 0):
            ang1shift = self.range2pi(ang1)
            ang2shift = self.range2pi(ang2)
            if not np.isclose(ang2shift, (ang1shift + angbtw)):
                return 2*np.pi - angbtw
            else: 
                return angbtw
        elif not np.isclose(ang2, (ang1 + angbtw)):
            return 2*np.pi - angbtw
        else:
            return angbtw
            
    def get_thetas_for_plotting(self, radius):
        "Calculates the thetas for plotting for a given radius"
        tempthetas_list = [] 
        for key,_ in self.radius_points_anglebetween_dict[radius].items():
            pntanglower = self.radius_point_angle_dict[radius][key[0]]
            pntangupper = self.radius_point_angle_dict[radius][key[1]]
            
            if pntanglower < pntangupper:
                tempthetas = np.linspace(pntanglower, pntangupper)
            # testing to capture all the cases
            elif pntanglower > pntangupper:
                if (pntanglower < 0) and (pntangupper < 0):
                    tempthetas = np.append(np.linspace(pntanglower, np.pi), np.linspace(np.pi, self.range2pi(pntangupper)))
                elif (pntanglower > 0) and (pntangupper > 0):
                    tempthetas = np.append(np.linspace(pntanglower, 2*np.pi), np.linspace(0,pntangupper))
                else:
                    tempthetas = np.linspace(self.range2pi(pntanglower), self.range2pi(pntangupper))
            tempthetas_list.append(tempthetas)
        return tempthetas_list

    def get_bisectors_between_points(self):
        "Calculates the bisector for all point pairs for all radii"
        self.radius_bisectorangs_dict = {}
        for rad, pntpair in self.radius_points_anglebetween_dict.items():
            self.radius_bisectorangs_dict[rad] = self._calculate_bisector_between_points(rad, pntpair)
        return self.radius_bisectorangs_dict
        
    def _calculate_bisector_between_points(self, rad, pointpair):
        "Calculates the bisector for pointpairs"
        tempbisectors = {}
        for pair, angbtw in pointpair.items():
            pntanglower = self.radius_point_angle_dict[rad][pair[0]]
            tempbisectors[pair] = (pntanglower + (angbtw/2))
        return tempbisectors
        
    def get_junction_opening_and_direction(self):
        "Calculate the opening angle and the bisector direction for each point pair of each radii"
        radius_opening_direction = {}
        for rad, pntpair in self.radius_points_anglebetween_dict.items():
            tempidx = np.argmin(list(pntpair.values()))
            tempopening = list(pntpair.values())[tempidx]
            tempbisector = self.range_neg_pi_to_pi(list(self.radius_bisectorangs_dict[rad].values())[tempidx])
            radius_opening_direction[rad] = {'opening_angle' : tempopening, 'bisector_direction' : tempbisector}
        self.center_radius_opening_direction = {self.point : radius_opening_direction}
        return self.center_radius_opening_direction

    def range2pi(self, ang):
        "Translate -pi and pi to 2pi range"
        return (ang+2*np.pi) % (2*np.pi)
        
    def range_neg_pi_to_pi(self, ang):
        "Translate 2 pi to -pi to pi"
        return (ang + np.pi) % (2*np.pi) - np.pi
        
    def unit_vector(self, vector):
        "Return unit vector"
        return vector / np.linalg.norm(vector)
    
    def angle_between(self, v1, v2):
        "Calculate the angle in radians between vectors"
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def plot_junction(self):
        "Plots the Yjunction and the angles"
        for l in self.lines:
            xl, yl = l.xy
            plt.plot(xl, yl, color='green', zorder=0)
        
        for radius, values in self.radius_point_angle_dict.items():
            # plot the radius
            radx = float(radius) * np.cos(np.linspace(0, 2*np.pi, 100)) + self.point.x
            rady = float(radius) * np.sin(np.linspace(0, 2*np.pi, 100)) + self.point.y
            plt.plot(radx, rady)
            # print(radius)
            # print(self.radius_points_anglebetween_dict[radius])
            for point, angles in values.items():
                # print(point)
                # plot the intersects and the angle
                plt.plot([self.point.x, point.x], [self.point.y, point.y], ls='dashed', color='black')
                plt.scatter(point.x,point.y, edgecolor='black',
                            facecolor='green', marker='P', s=100, zorder=5)
                thetas = self.get_thetas_for_plotting(radius)
                for i, theta in enumerate(thetas):
                    tempx = float(radius)*np.cos(theta)+self.point.x
                    tempy = float(radius)*np.sin(theta)+self.point.y
                    plt.plot(tempx, tempy, color="grey")
                    
                for i, (_, ang) in zip(range(len(self.radius_bisectorangs_dict[radius].items())), self.radius_bisectorangs_dict[radius].items()):
                            plt.plot([self.point.x, float(radius)*np.cos(ang)+self.point.x],
                                     [self.point.y, float(radius)*np.sin(ang)+self.point.y],
                                     color="grey")
                
        plt.scatter(self.point.x, self.point.y, color="black", zorder=6,
                    label='centre: {}, {}'.format(self.point.x, self.point.y))
        
        
        plt.xlim([self.point.x-float(radius)*1.1, self.point.x+float(radius)*1.1])
        plt.ylim([self.point.y-float(radius)*1.1, self.point.y+float(radius)*1.1])
        plt.gca().set_aspect('equal')
        plt.title('Max radius: {}'.format(radius))
        plt.legend(loc=1)
        plt.show()