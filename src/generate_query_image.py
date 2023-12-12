# 生成查询图像
# 将文件夹中某张图像添加噪声以作为查询图像
from PIL import Image
import numpy as np

# 读取图像
image_path = './img/5.jpg'
original_image = Image.open(image_path)
# 将图像转换为NumPy数组
image_array = np.array(original_image)

# 添加噪声
noise_factor = 1  # 调整噪声因子以控制噪声的强度
noise = np.random.normal(loc=0, scale=25, size=image_array.shape)
noisy_image_array = image_array + noise_factor * noise
# 将值限制在0到255之间
noisy_image_array = np.clip(noisy_image_array, 0, 255)
# 将NumPy数组转换回图像
noisy_image = Image.fromarray(np.uint8(noisy_image_array))

# 保存结果
output_path = './img/query_image.jpg'
noisy_image.save(output_path)


