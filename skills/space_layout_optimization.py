"""
Skill 1: 空间布局优化 (Space Layout Optimization)

功能：
- 分析房间尺寸、采光、通风等条件
- 生成最优的家具摆放方案
- 优化动线流线
- 划分功能区
"""

import os
import json
import logging
from typing import Dict, List, Any
import openai
from datetime import datetime

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

class SpaceLayoutOptimizer:
    def __init__(self):
        self.model = "gpt-4o"
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载 AI 提示词"""
        return {
            'analyze': '''你是一位专业的室内设计师。
根据以下房间信息，提供最优的空间布局优化方案：

房间信息：
- 房间类型: {room_type}
- 长度: {length}米
- 宽度: {width}米
- 高度: {height}米
- 窗户位置: {window_position}
- 房间用途: {purpose}
- 其他信息: {additional_info}

请提供以下内容（JSON格式）：
1. furniture_placement: 家具摆放建议（包括位置、尺寸）
2. flow_analysis: 动线流线分析
3. zoning: 功能区划分
4. lighting: 采光和通风建议
5. recommendations: 其他优化建议
6. alternative_plans: 2-3个备选方案'''
        }
    
    def optimize_layout(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化空间布局
        
        Args:
            room_data: 房间数据
                - room_type: 房间类型
                - length: 长度（米）
                - width: 宽度（米）
                - height: 高度（米）
                - window_position: 窗户位置
                - purpose: 房间用途
                - floorplan_image: 户型图（可选）
        
        Returns:
            Dict 包含优化方案
        """
        try:
            logger.info(f"开始优化布局: {room_data.get('room_type')}")
            
            # 构建提示词
            prompt = self.prompts['analyze'].format(
                room_type=room_data.get('room_type', 'living_room'),
                length=room_data.get('length', 5),
                width=room_data.get('width', 4),
                height=room_data.get('height', 2.8),
                window_position=room_data.get('window_position', 'south'),
                purpose=room_data.get('purpose', 'living'),
                additional_info=room_data.get('additional_info', '')
            )
            
            # 调用 OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是专业的室内设计师，提供基于数据的设计方案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result_text = response['choices'][0]['message']['content']
            
            # 解析 JSON 结果
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # 如果不是标准 JSON，创建结构化响应
                result = {
                    'raw_response': result_text,
                    'status': 'partial'
                }
            
            return {
                'success': True,
                'plan_id': f"layout_{datetime.now().timestamp()}",
                'room_type': room_data.get('room_type'),
                'layout_plan': result,
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'room_area': room_data.get('length', 0) * room_data.get('width', 0),
                    'ai_model': self.model,
                    'tokens_used': response['usage']['total_tokens']
                }
            }
        
        except Exception as e:
            logger.error(f"布局优化失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# 全局实例
_optimizer = SpaceLayoutOptimizer()

def optimize_layout_skill(room_data: Dict[str, Any]) -> Dict[str, Any]:
    """Skill 入口函数"""
    return _optimizer.optimize_layout(room_data)
