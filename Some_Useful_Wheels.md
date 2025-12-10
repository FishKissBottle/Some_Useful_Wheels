# Some Useful Wheels

尝试记录研究过程中的一些实用小工具/脚本

## 1 UseGdal ReadandWrite TifFile

### 1.1 功能

使用gdal的相关库读取与写入tif文件，处理的文件可以与Arcgis与ENVI等遥感软件协同使用。

### 1.2 需要安装的库

- numpy

```
pip install numpy==2.2.2
```

- gdal

  - gdal以及osgeo的安装直接使用pip安装貌似存在问题，因此建议从以下网址将安装包下载到本地：https://github.com/cgohlke/geospatial-wheels/releases。

  - 要展开"Assets"。

  - 若python版本未3.11，64位Windows操作系统，则寻找链接：gdal-3.11.4-cp311-cp311-win_arm64.whl，若为其他环境，则下载匹配的版本。

```
pip install <下载好的.whl文件的路径>
```

