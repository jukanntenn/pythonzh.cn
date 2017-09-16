# pythonzh.cn
为 Python 交流学习搭建的社区，使用 django1.10 和 Python3.5 强力驱动。

## 网站地址：
http://pythonzh.cn


## 在本地运行项目

1. 克隆项目到本地

   打开命令行，进入到保存项目的文件夹，输入如下命令：

   ```
   git clone https://github.com/zmrenwu/pythonzh.cn.git
   ```

2. 创建并激活虚拟环境

   在命令行进入到保存虚拟环境的文件夹，输入如下命令创建并激活虚拟环境：

   ```
   virtualenv pythonzhcn_env

   # windows
   pythonzhcn_env\Scripts\activate

   # linux
   source pythonzhcn_env/bin/activate
   ```

3. 安装项目依赖

   如果使用了虚拟环境，确保激活并进入了虚拟环境，在命令行进入项目所在的 pythonzh.cn 文件夹，运行如下命令：

   ```
   pip install -r requirements/base.txt
   ```

4. 迁移数据库

   在上一步所在的位置运行如下命令迁移数据库：

   ```
   python manage.py migrate
   ```

5. 创建后台管理员账户

   在上一步所在的位置运行如下命令创建后台管理员账户

   ```
   python manage.py createsuperuser
   ```

6. 运行开发服务器

   在上一步所在的位置运行如下命令开启开发服务器：

   ```
   python manage.py runserver --settings=config.settings.local
   ```

   在浏览器输入：127.0.0.1:8000

7. 进入后台

   在浏览器输入：127.0.0.1:8000/admin

   使用第 5 步创建的后台管理员账户登录