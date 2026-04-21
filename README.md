# 站长素材图片爬虫 (Chinaz Image Scraper)

一个功能完整的 Python 图片爬虫，用于从 `sc.chinaz.com` 下载图片。支持多页爬取、断点续爬、随机 User-Agent 和进度条显示。

## 功能特点

- 支持分页下载（用户可输入页数）
- 断点续爬：已下载的图片自动跳过，避免重复下载
- 随机 User-Agent 和请求延时，降低被反爬的风险
- 使用 `tqdm` 显示下载进度条，实时反馈
- 完善的异常处理，网络波动不会导致程序崩溃
- 图片文件名自动清洗，去除非法字符
- 模块化代码结构，易于理解和维护

## 安装依赖

确保你的 Python 版本 ≥ 3.8，然后安装所需库：

```bash
pip install requests lxml tqdm
```

使用方法

1. 将本项目代码下载到本地。
2. 打开终端，进入代码所在目录。
3. 运行主程序：

```bash
python chinaz_scraper.py
```

1. 根据提示输入要下载的页面数量，按回车开始下载。

下载的图片将自动保存在 img/ 文件夹中，文件名取自网页标题。

项目结构

```
.
├── chinaz_scraper.py   # 主程序
├── img/                # 下载的图片保存目录（自动创建）
└── README.md
```

技术栈

· Python 3.8+
· requests – 网络请求
· lxml – HTML 解析（XPath）
· tqdm – 进度条

注意事项

· 请遵守目标网站的 robots.txt 以及相关法律法规。
· 本代码已设置随机延时，请勿恶意高频请求，以免对服务器造成压力。
· 仅用于学习交流，不得用于商业用途。

作者

· GitHub: [Re-shenwenjun]
