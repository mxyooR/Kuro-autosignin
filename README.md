# Kuro-AutoSignin

自动化每日任务，轻松管理库街区论坛与游戏签到 

## 注意

仅供学习交流使用，请勿用于非法用途

## 获取 Token

为了更好地管理文件和依赖，获取 Token 功能已迁移至 [Kuro_login](https://github.com/mxyooR/Kuro_login)。请访问该项目以获取登录相关的详细说明和支持。

## 使用说明

1. **配置文件管理**  
   配置文件采用 YAML 格式存放于 `config` 目录中。每个用户对应一个 YAML 文件，文件名即用户的标识（不含扩展名）,如果需要多用户,复制`name.yaml.example`填写信息改成`name.yaml`放于 `config` 目录中。  
   - 配置文件包括用户基本信息、游戏信息（如 token、devcode、distinct_id、wwroleId、eeeroleId）以及用户状态（enable）。
   - 如果配置中未完整填写，系统会自动调用填充流程补全缺失信息。

   示例配置文件 `name.yaml.example`：
   ```yaml
   # 控制本 config 文件是否启用
   enable: true
   # token 必填
   token: ""
   # 是否完整，不完整默认系统自动补全
   completed: false
   # 是否自动补签
   auto_reple_sign: true
   
   # 游戏信息
   game_info:
     # distinct_id 和 devCode 可选，系统会随机生成
     distinct_id: ""
     devcode: ""
     # wwroleId：鸣潮 ID（可选，默认系统获取）
     wwroleId: 
     # eeeroleId：战双 ID（可选，默认系统获取）
     eeeroleId: 

   # 用户信息
   user_info:
     # 库街区 bbs ID（可选，默认系统获取）
     userId: ""
   ```

2. **签到流程**  
   主程序通过类 `SignInManager` 完成签到工作。  
   - 对于每个用户，系统先读取其 YAML 配置文件，检查是否启用和配置完整性。  
   - 执行游戏签到（鸣潮、战双）以及库街区签到，并根据结果记录日志。  
   - 如果签到返回信息中包含“用户信息异常”，系统会自动调用禁用操作，将该用户状态置为禁用。

3. **命令行参数**  
   运行时可添加 `--debug` 或 `--error` 参数以调整日志级别。

4. **签到信息推送**：如需要开启请在`config/push.ini`中设置`"enable":true`, 并且填写信息，填写`push_level`,推送详细程度：1=只推送总结，2=推送所有人的详细信息（一条），3=推送所有人的详细信息（多条）。具体参照[配置文档](/config/README.md)，感谢https://github.com/Womsxd/MihoyoBBSTools 项目提供推送方式.

5. **云函数支持**：入口为 `index.handler`。

6. **serverid设置**：战双serverid如果不对请自行抓包更正。


## 环境依赖

- Python 3.9 以上  
- 使用 `pip install -r requirements.txt` 安装依赖

## 运行方式

### 本地运行

1. **克隆项目**  
   将项目克隆到本地目录：
   ```bash
   git clone https://github.com/mxyooR/Kuro-autosignin.git
   cd Kuro-autosignin
   ```

2. **安装依赖**  
   使用 pip 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. **配置文件**  
   在 `config` 目录下创建或修改 YAML 配置文件（如 `name.yaml`），填写必要的用户信息。

4. **运行程序**  
   执行以下命令运行主程序：
   ```bash
   python main.py
   ```

5. **调试模式**（可选）  
   如果需要调试日志信息，可以添加 `--debug` 参数：
   ```bash
   python main.py --debug
   ```

6. **查看日志**  
   程序运行后，日志文件会保存在 `logs` 目录下，可通过日志文件查看运行结果。

### 青龙面板运行方法

1. **拉取项目到本地**  
   将项目克隆到本地目录。

2. **获取个人信息**  
   捕获库街区的包，按照本地部署的方式获取你需要的个人信息，并填写到 `config` 目录下的 `name.yaml` 文件中（每个用户一个 YAML 文件，文件名为用户标识，不含扩展名）。

3. **创建订阅**  
   在青龙面板中创建新的订阅任务：
   - 名称：库街区签到
   - 类型：公开仓库
   - 链接：<https://github.com/mxyooR/Kuro-autosignin.git>
   - 定时类型：crontab
   - 定时规则：1 9 * * *
   - 白名单：ql_main.py
   - 依赖文件：log|game_check_in|bbs_sign_in|push|tools|config

4. **导入配置文件**  
   在青龙面板的脚本管理中，进入 `mxyooR_Kuro-autiosignin/config` 文件目录下，导入并替换修改好的 `name.yaml` 文件。

5. **添加依赖**  
   在青龙面板的依赖管理中安装所需的 Python 第三方库（例如 requests）。

6. **推送选项**  
   推送设置请在 `config/push.ini` 中配置，确认其中推送开关（enable）以及推送等级（push_level）已正确设置。  
   - 如果使用本项目内置的推送，请确保白名单修改成 `main.py`，且将 `push.ini` 文件放置于 `config` 目录下。

## Docker 运行方法

### 说明
1. **基础镜像**：使用 `python:3.9-slim` 作为基础镜像，轻量级且适合生产环境。
2. **工作目录**：将工作目录设置为 `/app`。
3. **配置文件**：在本地设置好`config`配置文件，替换个人信息。
4. **复制文件**：将项目文件复制到容器中。
5. **安装依赖**：通过 `requirements.txt` 安装自动签到的项目依赖。
6. **运行程序**：默认运行 `main.py`，你可以根据需要修改。

---

### 构建和运行 Docker 容器

1. **克隆代码**：
   ```bash
   git clone https://github.com/mxyooR/Kuro-autosignin.git
   cd Kuro-autosignin
   ```
  
2. **构建镜像**：
   ```bash
   docker build -t kuro-autosignin .
   ```

3. **运行容器**：
   ```bash
   docker run -d --name kuro-autosignin-container kuro-autosignin
   ```

4. **查看日志**：
   ```bash
   docker logs kuro-autosignin-container
   ```

---

### 使用 Docker Compose（可选）
如果你希望更方便地管理容器，可以使用 Docker Compose。

1. **创建 `docker-compose.yml` 文件**：
   ```yaml
   version: '3.8'
   services:
     kuro-autosignin:
       build: .
       container_name: kuro-autosignin-container
       environment:
         - CRON_SIGNIN=30 9 * * *
         - TZ=Asia/Shanghai
       volumes:
         - ./config:/app/config
       restart: unless-stopped
   ```

2. **启动容器**：
   ```bash
   docker-compose up -d
   ```

3. **查看日志**：
   ```bash
   docker-compose logs -f
   ```

4. **更新镜像**：
   ```bash
   docker-compose stop
   docker-compose pull && docker-compose up -d




