import os
import yaml
import uuid
from log import log_info, log_error
from tools import get_user_info_by_token, get_game_user_id

class ConfigManager:
    def __init__(self, config_dir=None):
        """
        初始化配置管理器
        :param config_dir: 配置目录，如果为None则尝试从环境变量获取
        """
        # 检查是否在青龙环境中运行
        # 青龙不传config_dir参数进来
        ql_config_path = os.environ.get('KuroBBS_config_path', '')
        
        # 如果提供了config_dir参数，优先使用
        if config_dir:
            self.config_dir = config_dir
        elif ql_config_path:
            self.config_dir = ql_config_path
            log_info(f"使用环境变量配置路径: {self.config_dir}")
        else:
            # 默认路径是当前工作目录下的config文件夹
            self.config_dir = os.path.join(os.getcwd(), "config")
            log_info(f"使用默认配置路径: {self.config_dir}")
        
        # 确保配置目录存在
        os.makedirs(self.config_dir, exist_ok=True)
        
        # 获取配置文件前缀
        self.config_prefix = os.environ.get('KuroBBS_config_prefix', '')
        if self.config_prefix:
            log_info(f"配置文件将使用前缀: {self.config_prefix}")

    def load_user_config(self, user_name):
        """
        加载指定用户的 YAML 配置文件
        :param user_name: 用户名（文件名，不含扩展名）
        :return: 用户配置数据
        """
        config_path = os.path.join(self.config_dir, f"{user_name}.yaml")
        if not os.path.exists(config_path):
            log_error(f"配置文件不存在: {config_path}")
            return None
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            return yaml.safe_load(f)

    def update_user_config(self, user_name, key, value):
        """
        更新指定用户的配置文件
        :param user_name: 用户名（文件名，不含扩展名）
        :param key: 要更新的键
        :param value: 新值
        """
        config_path = os.path.join(self.config_dir, f"{user_name}.yaml")
        if not os.path.exists(config_path):
            log_error(f"配置文件不存在: {config_path}")
            return
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f)
        data[key] = value
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)
        log_info(f"已更新 {user_name} 的配置: {key} = {value}")

    def disable_user(self, user_name):
        """
        禁用指定用户
        :param user_name: 用户名（文件名，不含扩展名）
        """
        self.update_user_config(user_name, "enable", False)

    def fill_raw_config(self, user_name, token, devcode=None, distinct_id=None):
        """
        填充原始 YAML 格式的配置文件
        更新 game_info 中的 token, devCode 以及 distinct_id
        :param user_name: 用户名（文件名，不含扩展名）
        :param token: 用户 token
        :param devcode: 设备代码（可选）
        :param distinct_id: 唯一标识符（可选）
        """
        config_path = os.path.join(self.config_dir, f"{user_name}.yaml")
        if not os.path.exists(config_path):
            log_error(f"配置文件不存在: {config_path}")
            return

        try:
            with open(config_path, 'r', encoding='utf-8-sig') as f:
                config_data = yaml.safe_load(f)

            if not config_data:
                config_data = {}

            # 如果未提供 devcode 和 distinct_id，则生成随机值
            devcode = devcode or str(uuid.uuid4())
            distinct_id = distinct_id or str(uuid.uuid4())

            # 更新 game_info 部分
            if 'game_info' not in config_data:
                config_data['game_info'] = {}
            config_data['game_info']['devcode'] = devcode
            config_data['game_info']['distinct_id'] = distinct_id

            # 更新 user_info 部分
            if 'user_info' not in config_data:
                config_data['user_info'] = {}
            config_data['user_info']['userId'] = get_user_info_by_token(token, devcode, distinct_id)

            # 更新 game_id
            ww_role_id = get_game_user_id(token, 3, devcode, distinct_id)
            eee_role_id = get_game_user_id(token, 2, devcode, distinct_id)
            config_data['game_info']["wwroleId"] = ww_role_id
            config_data['game_info']["eeeroleId"] = eee_role_id

            config_data['completed'] = True
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config_data, f, allow_unicode=True, default_flow_style=False)

            log_info(f"{user_name} 的 YAML 配置文件已成功填充")
        except Exception as e:
            log_error(f"填充 YAML 配置文件失败: {e}")

    def disable_user_config(self, user_name):
        """
        禁用指定用户的配置文件
        :param user_name: 用户名（文件名，不含扩展名）
        """
        # 检查是否应该禁用该配置文件
        # 如果设置了前缀且不匹配，则跳过（保留MihoyoBBS工具配置）
        if self.config_prefix and not user_name.startswith(self.config_prefix):
            log_info(f"未禁用非前缀配置文件: {user_name}.yaml (保留MihoyoBBS工具配置)")
            return
        
        config_path = os.path.join(self.config_dir, f"{user_name}.yaml")
        if not os.path.exists(config_path):
            log_error(f"配置文件不存在: {config_path}")
            return

        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                data = yaml.safe_load(f)

            data["enable"] = False  # 将 enable 设置为 False

            with open(config_path, 'w', encoding="utf-8-sig") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

            log_info(f"{user_name} 的用户状态已成功更新为禁用")
        except Exception as e:
            log_error(f"更新用户状态失败: {e}")
            log_error(f"更新用户状态失败: {e}")
