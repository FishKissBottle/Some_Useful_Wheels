from osgeo import gdal, osr     
import numpy as np


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
        dataset = gdal.Open(input_data_path)
        img_width = dataset.RasterXSize                                 # tif文件的宽度 // The width of the Tif file
        img_height = dataset.RasterYSize                                # tif文件的高度 // The height of the Tif file
        img_proj = dataset.GetProjection()                              # tif文件的投影坐标 // The projection coordinates of the Tif file
        img_trans = dataset.GetGeoTransform()                           # tif文件的仿射矩阵 // The affine matrix of a Tif file
        img_data = dataset.ReadAsArray(0, 0, img_width, img_height)     # 读取tif文件中的像元信息 // Read the pixel information in the Tif file

        dataset.FlushCache()                                            # 强制性地清除缓存 // Forcibly clear the cache
        dataset = None                                                  # 释放文件句柄 // Release the file handle

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
            img_bands, rows, cols = img_data.shape
        else:
            img_bands, (rows, cols) = 1, img_data.shape

        # 计算trans参数，注意要pixel_height取负值，因为纬度递增时像素坐标递减 // Calculate the trans parameters, pixel_height should take a negative number
        geotransform = (top_left_lon, pixel_width, 0, top_left_lat, 0, pixel_height)

        # 创建输出 TIF 文件 // Create an output TIF file
        driver = gdal.GetDriverByName("GTiff")
        output_dataset = driver.Create(output_path, cols, rows, img_bands, gdal.GDT_Float32)

        # 设置地理转换 // Set geographical conversion
        output_dataset.SetGeoTransform(geotransform)

        # 设置坐标系的EPSG代码(WGS84的EPSG代码为4326) // Set the EPSG code for the coordinate system (The EPSG code for WGS84 is 4326)
        output_srs = osr.SpatialReference()
        output_srs.ImportFromEPSG(epsg_code)
        output_dataset.SetProjection(output_srs.ExportToWkt())

        # 写入数据 // Write data into output_dataset
        if img_bands == 1:
            output_band = output_dataset.GetRasterBand(1)
            output_band.SetNoDataValue(nodata_value)
            output_band.WriteArray(img_data)
        else:
            for i in range(img_bands):
                output_band = output_dataset.GetRasterBand(i + 1)
                output_band.SetNoDataValue(nodata_value)
                output_band.WriteArray(img_data[i])

        # 生成金字塔，使用双线性插值 // Generate the pyramid using bilinear interpolation
        output_dataset.BuildOverviews("BILINEAR", [2, 4, 8, 16])

        # 关闭数据集 // Close output_dataset
        del output_dataset
