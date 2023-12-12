import os
from PIL import Image
import numpy as np
import tenseal as ts
import time

# 读取文件夹中所有图像
image_folder = "./img/"
image_files = os.listdir(image_folder)

# 准备加密环境使用CKKS
ctx = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[40, 21, 21, 21, 21, 21, 21, 40])
sk = ctx.secret_key()
ctx.make_context_public()

# 加密查询图像
query_image_path = "./img/query_image.jpg"
query_img = Image.open(query_image_path).convert('L')
query_img = query_img.resize((64, 64))
query_img_array = np.array(query_img)
query_img_vector = query_img_array.flatten()

# 设置全局尺度
global_scale = 2**40
ctx.global_scale = global_scale

encrypted_query_vector = ts.ckks_vector(ctx, query_img_vector)

# 初始化最小差异值和对应的图像名
min_diff = float('inf')
min_diff_image_name = ""

# 记录开始时间
start_time = time.time()  

# 计算每个图像与查询图像的差异向量及其平均绝对值
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    # 打开图像并转换为灰度图像
    img = Image.open(image_path).convert('L')  
    # 将图像大小调整为64x64
    img = img.resize((64, 64))  
    # 将图像转换为浮点向量形式并加密
    img_array = np.array(img)
    img_vector = img_array.flatten()  
    # 将图像转换为一维浮点向量
    encrypted_vector = ts.ckks_vector(ctx, img_vector)
    # 计算与查询图像的差异向量
    diff_vector = encrypted_vector - encrypted_query_vector
    # 解密差异向量
    decrypted_diff = diff_vector.decrypt(sk) 
    # 计算差异向量的绝对值和平均值
    abs_diff = np.abs(decrypted_diff)
    mean_diff = np.mean(abs_diff)
    # 输出每张图像的平均差异值
    print(f"{image_file} 的平均差异值：{mean_diff}")
    if image_file == "query_image.jpg":
        continue
    # 找到差异值最小的图像
    if mean_diff < min_diff:
        min_diff = mean_diff
        min_diff_image_name = image_file

# 记录结束时间
end_time = time.time()  
# 计算执行时间
execution_time = end_time - start_time  
print(f"CKKS算法消耗时间为：{execution_time} 秒")

# 输出最小差异值不为零的图像名
print(f"差异值最小的图像是：{min_diff_image_name}，其平均差异值为：{min_diff}")
