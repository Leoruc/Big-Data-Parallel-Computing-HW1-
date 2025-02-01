#include <opencv2/opencv.hpp> // 用于图像处理
#include <omp.h>
#include <stdio.h>
#include <chrono>  // 用于高精度计时
#include <sys/stat.h>  // 用于创建目录

int main() 
{
    int num_images = 100;
    char file_prefix[] = "output";
    char file_suffix[] = ".png";
    char output_folder[] = "output_edges";  // 输出文件夹

    // 创建输出文件夹（如果不存在）
    struct stat st = {0};
    if (stat(output_folder, &st) == -1) {
        mkdir(output_folder, 0700);  
    }

    // 开始计时
    auto start_time = std::chrono::high_resolution_clock::now();

    #pragma omp parallel for // 并行加快速度(将这行命令删除便是串行版本)
    for (int i = 1; i <= num_images; ++i) {
        // 设置读入图像的名称
        char file_name[50];
        snprintf(file_name, sizeof(file_name), "%s%d%s", file_prefix, i, file_suffix);
        
        // 读入图像
        cv::Mat img = cv::imread(file_name, cv::IMREAD_COLOR);

        // 转换为灰度图像
        cv::Mat gray;
        cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);

        // 边缘检测
        cv::Mat edges;
        cv::Canny(gray, edges, 100, 200);

        // 设置输出图像的名称，包括指定文件夹
        char output_name[100];
        snprintf(output_name, sizeof(output_name), "%s/edges_%d.png", output_folder, i);

        // 保存边缘检测结果图像
        cv::imwrite(output_name, edges);
    }

    // 结束计时
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_time = end_time - start_time;

    // 输出时长
    printf("边缘检测时长: %f 秒\n", elapsed_time.count());

    return 0;
}



