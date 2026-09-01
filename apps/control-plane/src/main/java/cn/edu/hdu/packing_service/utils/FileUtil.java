package cn.edu.hdu.packing_service.utils;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/1/30 13:56
 */
public class FileUtil {

    /**
     * @Author: strelizia
     * @Date: 2024/1/30 14:02
     * @param: folderPath
     * @return: List<String>
     * @Description: 获取文件夹下所有文件名
     */
    public static List<String> getALlFilesName(String folderPath){
        File folder = new File(folderPath);
        List<String> fileNames = new ArrayList<>();

        File[] listOfFiles = folder.listFiles();
        if (listOfFiles != null) {
            for (File file : listOfFiles) {
                if (file.isFile()) {
                    fileNames.add(file.getName());
                }
            }
        }
        return fileNames;
    }
}
