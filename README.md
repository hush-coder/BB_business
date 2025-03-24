# 商业平台

这是一个连接工厂和经销商的商业平台，提供产品展示、在线沟通和交易管理等功能。

## 功能特点

- 三种用户角色：管理员、工厂、经销商
- 工厂可以发布产品信息
- 经销商可以浏览产品并与工厂沟通
- 管理员可以管理用户和产品信息
- 实时消息系统
- 响应式设计，支持移动端访问

## 安装说明

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd [项目目录]
```

2. 创建并激活conda环境：
```bash
conda create -n business python=3.8
conda activate business
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 设置环境变量（可选）：
```bash
# Windows
set SECRET_KEY=your-secret-key
set ADMIN_INVITE_CODE=your-admin-code

# Linux/Mac
export SECRET_KEY=your-secret-key
export ADMIN_INVITE_CODE=your-admin-code
```

5. 初始化数据库：
```bash
flask db init
flask db migrate
flask db upgrade
```

6. 运行应用：
```bash
python app.py
```

## 使用说明

1. 访问 http://localhost:5000 打开应用
2. 注册新账号（选择相应角色）
3. 登录系统
4. 根据角色使用相应功能

## 角色权限

### 管理员
- 查看所有用户信息
- 管理产品信息
- 审核经销商申请
- 系统维护

### 工厂
- 发布产品信息
- 管理自己的产品
- 与经销商沟通
- 查看收到的消息

### 经销商
- 浏览产品信息
- 与工厂沟通
- 查看收到的消息
- 管理个人信息

## 技术栈

- 后端：Python Flask
- 数据库：SQLite
- 前端：Bootstrap 5
- 认证：Flask-Login
- 表单：Flask-WTF

## 开发团队

[团队信息]

## 许可证

MIT License