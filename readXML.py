import xml.etree.ElementTree as ET
import pandas as pd

xml_file = r"C:\Users\matte\Downloads\Mark_analysis_output.xml"

def get_coords_df(xml_file):
    xml_file = r"C:\Users\matte\Downloads\Mark_analysis_output.xml"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    regions = []
    markers = []
    markers_x, markers_y, markers_z = [], [], []
    x_points, y_points, z_points = [], [], []
    for child in root:
        if 'name' in child.attrib.keys():
            region_name = child.attrib.get('name').replace(",", "").lower()
            subchildren = child.findall('{https://www.mbfbioscience.com/filespecification}point')
            if 'marker' in region_name.lower():
                markers += [region_name] * len(subchildren)
                for point in subchildren:
                    markers_x.append(float(point.attrib.get('x')))
                    markers_y.append(float(point.attrib.get('y')))
                    markers_z.append(float(point.attrib.get('z')))
            else:
                regions += [region_name] * len(subchildren)
                for point in subchildren:
                    x_points.append(float(point.attrib.get('x')))
                    y_points.append(float(point.attrib.get('y')))
                    z_points.append(float(point.attrib.get('z')))

    markers_df = pd.DataFrame({'Marker': markers, 'x': markers_x, 'y': markers_y, 'z':markers_z})
    positions_df = pd.DataFrame({'Region Name': regions, 'x':x_points, 'y': y_points, 'z': z_points})
    allen_csv = pd.read_csv(r"C:\Users\matte\Downloads\structure_tree_safe_2017.csv")
    allen_csv['name'] = allen_csv['name'].apply(lambda x: x.lower())
    allen_csv = allen_csv.loc[:, ['name', 'acronym', 'id']]
    allen_csv.rename(columns={'name': 'Region Name'}, inplace=True)
    positions_df = pd.merge(positions_df, allen_csv, on=['Region Name'])
    return positions_df, markers_df