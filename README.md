# Kuro-AutoSignin

自动化每日任务，轻松管理库街区论坛与游戏签到 

## 注意

仅供学习交流使用，请勿用于非法用途

## 获取 Token

为了更好地管理文件和依赖，获取 Token 功能已迁移至 [Kuro_login](https://github.com/mxyooR/Kuro_login)。请访问该项目以获取登录相关的详细说明和支持。

## 使用说明

1. **配置文件管理**  
   配置文件采用 YAML 格式存放于 `config` 目录中。每个用户对应一个 YAML 文件，文件名即用户的标识（不含扩展名）。  
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
   
   # 重试次数（失败后再次尝试的总次数，默认 3）
   retry_times: 3

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
   主程序通过 `SignInManager` 完成签到工作。  
   - 对于每个用户，系统先读取其 YAML 配置文件，检查是否启用和配置完整性。  
   - 执行游戏签到（鸣潮、战双）以及库街区签到，并根据结果记录日志。  
   - 如果签到返回信息中包含"用户信息异常"或"登录已过期"，系统会自动调用禁用操作，将该用户状态置为禁用。

3. **命令行参数**  
   运行时可添加 `--debug` 或 `--error` 参数以调整日志级别。

4. **签到信息推送**  
   如需要开启请在 `config/push.ini` 中设置 `"enable":true`，并填写信息，填写 `push_level`，推送详细程度：1=只推送总结，2=推送所有人的详细信息（一条），3=推送所有人的详细信息（多条）。具体参照[配置文档](/config/README.md)。


5. **serverid设置**：战双serverid如果不对请自行抓包更正。


---

## 云函数运行方法


### 一、准备工作

1. **拉取项目**
   ```bash
   git clone https://github.com/mxyooR/Kuro-autosignin.git
   cd Kuro-autosignin
   ```

 

2. **安装依赖**
   确保项目依赖已安装：
   ```bash
   pip install . -t .
   ```

3. **配置文件**
   在 `config` 目录下创建或修改 YAML 配置文件（如 `name.yaml`），填写必要的用户信息。

4. **推送配置**
   如果需要推送功能，请在 `config/push.ini` 中配置推送服务。

---

### 二、云函数入口

云函数的入口 `index.handler` 



### 三、部署到云函数平台

#### 1. 腾讯云函数（SCF）

1. **登录腾讯云函数控制台**  
   访问 [腾讯云函数控制台](https://console.cloud.tencent.com/scf) 并登录。

2. **创建函数**
   - 函数类型：自定义创建。
   - 运行环境：Python 3.10。
   - 上传代码：将项目文件打包为 ZIP 文件上传。
   - 函数入口：`index.handler`。


3. **测试运行**
   在函数管理页面，点击“测试”按钮，查看日志输出是否正常。

---

#### 2. 阿里云函数计算（FC）

1. **登录阿里云函数计算控制台**  
   访问 [阿里云函数计算控制台](https://fc.console.aliyun.com/) 并登录。

2. **创建服务和函数**
   - 服务名称：自定义。
   - 函数名称：自定义。
   - 运行环境：Python 3.10。
   - 上传代码：将项目文件打包为 ZIP 文件上传。
   - 函数入口：`index.handler`。


3. **测试运行**
   在函数管理页面，点击“测试”按钮，查看日志输出是否正常。

---

### 四、定时触发器

为云函数添加定时触发器，实现每日自动签到。

#### 腾讯云
1. 在函数管理页面，点击“触发管理”。
2. 添加触发器，选择“定时触发”。
3. 设置触发周期（如每天早上7点）。

#### 阿里云
1. 在函数管理页面，点击“触发器”。
2. 添加触发器，选择“定时触发”。
3. 设置触发规则（如每天早上7点）。

---

### 五、查看日志

运行后可以在云函数的日志服务中查看执行结果，排查可能的问题。

---

## 环境依赖

- Python 3.9 以上  
- 使用 `pip install .` 安装依赖

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
   pip install .
   ```
> [!IMPORTANT]
> 如果您需要用到Windows的推送功能，请使用以下命令安装依赖：
> ```pip install .[windows]```

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

青龙面板是一个支持定时任务的面板工具，可以稳定运行库街区签到。以下是详细配置步骤：

#### 一、拉取代码

在青龙面板的"订阅管理"中添加：

- 名称：库街区签到
- 类型：公开仓库
- 链接：https://github.com/mxyooR/Kuro-autosignin.git
- 定时类型：crontab
- 定时规则：1 7 * * *  (每天早上7:01执行)
- 白名单：ql_main.py
- 依赖文件：log|push|tools|constants|models|http_client|config_manager|game_sign_in|forum_sign_in|sign_in_manager|main

或者使用命令行添加：

```bash
ql repo https://github.com/mxyooR/Kuro-autosignin.git "ql_main.py" "" "log|push|tools|constants|models|http_client|config_manager|game_sign_in|forum_sign_in|sign_in_manager|main"
```

#### 二、环境变量配置

在青龙面板的"环境变量"中添加以下变量：

| 名称 | 值 | 说明 |
| ---- | ---- | ---- |
| KuroBBS_config_path | /ql/data/config/ | 配置文件存放路径 |
| KuroBBS_log_level | INFO | 日志级别(INFO/DEBUG/ERROR) |
| KuroBBS_push_project | 0/1 | 是否使用项目自带推送(1=是) |
| KuroBBS_push_path | /ql/data/config/ | 推送配置文件路径(选填) |
| KuroBBS_config_prefix | kjq_ | 配置文件前缀(选填)，设置后只处理有此前缀的配置文件，可避免与其他工具的配置文件冲突 |


#### 三、添加配置文件

1. 进入青龙容器：
   ```bash
   docker exec -it qinglong bash
   ```

2. 复制配置文件模板：
   ```bash
   cp /ql/data/repo/mxyooR_Kuro-autosignin/config/name.yaml.example /ql/data/config/name.yaml
   ```

3. 编辑配置文件，填入你的库街区token：
   ```bash
   vi /ql/data/config/name.yaml
   ```

4. 复制并配置推送文件：
   ```bash
   cp /ql/data/repo/mxyooR_Kuro-autosignin/config/push.ini.example /ql/data/config/push.ini
   vi /ql/data/config/push.ini
   ```

#### 四、安装依赖

在青龙面板的"依赖管理"->"Python"中添加：
- requests
- pyyaml
- pytz
- httpx

#### 五、运行任务

完成上述配置后，可以在"定时任务"中找到并运行"库街区签到"任务进行测试。

#### 六、查看日志

运行后可以在任务日志中查看执行结果，排查可能的问题。

## Docker 运行方法

### 说明
1. **基础镜像**：使用 `python:3.9-slim` 作为基础镜像，轻量级且适合生产环境。
2. **工作目录**：将工作目录设置为 `/app`。
3. **配置文件**：在本地设置好`config`配置文件，替换个人信息。
4. **复制文件**：将项目文件复制到容器中。
5. **安装依赖**：通过 `pyproject.toml` 安装自动签到的项目依赖。
6. **运行程序**：默认运行 `main.py`，你可以根据需要修改。

---

### 构建和运行 Docker 容器

1. **克隆代码**：
   ```bash
   git clone https://github.com/mxyooR/Kuro-autosignin.git
   cd Kuro-autosignin
   ```

2. **修改定时信息**（可选）：\
   如果需要修改定时任务，可以在 `Dockerfile` 中的 `ENV CRON_SIGNIN` 行进行修改，格式为标准的 cron 表达式。例如，设置为每天早上9:30：
    ```dockerfile
    ENV CRON_SIGNIN="30 9 * * *"
    ```
  
3. **构建镜像**：
   ```bash
   docker build -t kuro-autosignin .
   ```

4. **运行容器**：
   ```bash
   docker run -d --name kuro-autosignin-container kuro-autosignin
   ```

5. **查看日志**：
   ```bash
   docker logs kuro-autosignin-container
   ```

---

### 使用 Docker Compose（可选）
如果你希望更方便地管理容器，可以使用 Docker Compose。

1. **修改 `docker-compose.yml` 文件**：
   与上文Dockerfile文件相同，此文件中的 `CRON_SIGNIN` 环境变量可以根据需要修改。
   ```yaml
   - CRON_SIGNIN=30 9 * * *
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
   ```
