from osgeo import gdal, osr     
import numpy as np
import rasterio
from pyproj import CRS as pyprojCRS


class Tif_Read_and_Write(object):
    def __init__(self):
        super().__init__()

    def Tif_Read(self, 
                 input_data_path: str):
        '''
        input_data_path: 输入需要读取tif文件的路径
        -------------------
        input_data_path: Input Tif file path
        '''
        # 读取数据
        with rasterio.open(input_data_path) as src:
            img_data = src.read()
            img_proj = src.crs
            img_trans = src.transform
            
        return img_data, img_proj, img_trans


    def Numpy_to_Tif(self, 
                     img_data: np.ndarray, 
                     output_path: str, 
                     top_left_lon: float, 
                     top_left_lat: float, 
                     pixel_width: float, 
                     pixel_height: float, 
                     epsg_code: int, 
                     nodata_value: int | float | np.ndarray = np.nan):
        '''
        img_data: 一个ndarray矩阵
        output_path: 输出Tif文件的路径
        top_left_lon: ndarray矩阵左上角像元的左上角的经度值
        top_left_lat: ndarray矩阵左上角像元的左上角的纬度值
        pixel_width: Tif中每个像元的宽度
        pixel_height: Tif中每个像元的高度
        epsg_code: 坐标系的EPSG代码
        nodata_value: Tif中的无效值，默认为np.nan
        -------------------
        img_data: An ndarray matrix
        output_path: Output Tif file path
        top_left_lon: The longitude value in the upper left corner of the ndarray matrix
        top_left_lat: The latitude value in the upper left corner of the ndarray matrix
        pixel_width: The width of each pixel in the Tif file
        pixel_height: The height of each pixel in the Tif file
        epsg_code: The EPSG code of the coordinate system
        nodata_value: Nodata values in Tif files, defaulting to np.nan   
        '''
        # 判断传入数据的维数，是单波段还是多波段 // Determine the dimension of the img_data, whether it is single-band or multi-band
        if len(img_data.shape) == 3:  
            img_bands, img_rows, img_cols = img_data.shape
        else:
            img_bands, (img_rows, img_cols) = 1, img_data.shape

        # trans参数，注意要pixel_height取负值 // For the trans parameter, note that pixel_height should be set to a negative value
        # | a b c |
        # | d e f |
        # | 0 0 1 |
        # a：像素宽度（x方向每个像素代表的地理距离） // a: Pixel width
        # b：行旋转（通常为0） // b: Row rotation
        # c：左上角像素的x坐标 // c: The x-coordinate of the pixel in the upper left corner
        # d：列旋转（通常为0） // d: Column rotation
        # e：像素高度（y方向每个像素代表的地理距离，通常为负值） // e: Pixel height
        # f：左上角像素的y坐标 // f: The y-coordinate of the pixel in the upper left corner
        geotransform = (pixel_width, 0.0, top_left_lon, 0.0, -pixel_height, top_left_lat)
        proj = rasterio.crs.CRS.from_wkt(pyprojCRS.from_epsg(epsg_code).to_wkt())

        profile = {
            'driver': 'GTiff',                   # 文件格式
            'dtype': img_data.dtype,             # 数据类型
            'nodata': nodata_value,              # 无数据值 (可选，这里假设没有)
            'width': img_cols,                   # 宽度 (列数)
            'height': img_rows,                  # 高度 (行数)
            'count': img_bands,                  # 波段数
            'crs': proj,                         # 坐标参考系统
            'transform': geotransform,           # 仿射变换
            'compress': 'lzw',                   # 压缩方式 (可选)
        }           

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(img_data)


# -------------------示例-------------------
# >>> 读取
data, prj, trans = Tif_Read_and_Write().Tif_Read(input_data_path=r'./sample_file.tif')
# >>> 存储
Tif_Read_and_Write().Numpy_to_Tif(img_data=data, 
                                  output_path=r'./new_sample_file.tif', 
                                  top_left_lon=0.0, 
                                  top_left_lat=0.0, 
                                  pixel_width=0.01, 
                                  pixel_height=0.01, 
                                  epsg_code=4326，
                                  nodata_value=np.nan)