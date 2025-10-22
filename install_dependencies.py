#!/usr/bin/env python3
"""
安装Python依赖包 - 使用国内镜像源
"""

import subprocess
import sys
import time

def install_package(package, retries=3):
    """安装指定的Python包，使用国内镜像源"""
    mirrors = [
        "https://pypi.tuna.tsinghua.edu.cn/simple",
        "https://mirrors.aliyun.com/pypi/simple/", 
        "https://pypi.mirrors.ustc.edu.cn/simple/",
        "https://pypi.douban.com/simple/"
    ]
    
    for attempt in range(retries):
        for mirror in mirrors:
            try:
                print(f"尝试从 {mirror} 安装 {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package,
                    "-i", mirror, "--trusted-host", mirror.split('/')[2],
                    "--timeout", "300",  # 增加超时时间到5分钟
                    "--retries", "3"     # 重试3次
                ])
                print(f"✅ 成功安装: {package}")
                return True
            except subprocess.CalledProcessError:
                print(f"❌ 从 {mirror} 安装失败，尝试下一个镜像...")
                continue
            except Exception as e:
                print(f"❌ 安装异常: {e}")
                continue
        
        if attempt < retries - 1:
            wait_time = (attempt + 1) * 10  # 递增等待时间
            print(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    print(f"❌ 所有镜像都安装失败: {package}")
    return False

def main():
    """主函数"""
    print("安装性能分析所需的Python依赖包...")
    print("使用国内镜像源以加速下载...")
    
    # 基础依赖包（必须）
    essential_packages = [
        'pandas',
        'matplotlib', 
        'seaborn',
        'scipy',
        'openpyxl'  # 用于Excel输出
    ]
    
    # 可选依赖包（如果安装失败可以跳过）
    optional_packages = [
        'scienceplots'  # 科学论文风格的图表
    ]
    
    success_count = 0
    essential_success = 0
    
    # 先安装基础依赖
    print("\n安装基础依赖包...")
    for package in essential_packages:
        if install_package(package):
            success_count += 1
            essential_success += 1
    
    # 然后安装可选依赖
    print("\n安装可选依赖包...")
    for package in optional_packages:
        if install_package(package, retries=2):  # 可选包重试次数减少
            success_count += 1
    
    print(f"\n安装完成: {success_count}/{len(essential_packages) + len(optional_packages)} 个包成功安装")
    
    if essential_success == len(essential_packages):
        print("🎉 所有基础依赖包安装成功!")
        print("✅ 系统可以正常运行!")
    else:
        print(f"⚠️  基础依赖包安装: {essential_success}/{len(essential_packages)}")
        print("❌ 部分基础功能可能无法使用")
    
    # 提供备选方案
    if essential_success < len(essential_packages):
        print("\n备选方案:")
        print("1. 手动安装: pip install pandas matplotlib seaborn scipy openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple")
        print("2. 使用系统包管理器: sudo apt install python3-pandas python3-matplotlib python3-seaborn")
        print("3. 使用conda: conda install pandas matplotlib seaborn scipy openpyxl")

if __name__ == "__main__":
    main()
