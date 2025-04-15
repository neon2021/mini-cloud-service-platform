import asyncio
import importlib.util
import sys
import logging
from pathlib import Path
from typing import Any, Dict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LambdaRuntime:
    @staticmethod
    async def invoke(function_path: Path, event: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 动态加载函数模块
            spec = importlib.util.spec_from_file_location("lambda_function", function_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["lambda_function"] = module
            spec.loader.exec_module(module)

            # 获取函数处理器
            handler = getattr(module, "lambda_handler")
            
            # 在事件循环中执行函数
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, handler, event, None)
            
            return result
        except Exception as e:
            logger.error(f"Failed to execute function: {str(e)}")
            raise 