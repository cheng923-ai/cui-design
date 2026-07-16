"""
Skill 2: 颜色搭配推荐 (Color Matching)

功能：
- 根据风格生成颜色方案
- 提供主色、辅色、点缀色
- 生成色彩心理学解释
- 支持参考图片分析
"""

import os
import json
import logging
from typing import Dict, List, Any
import openai
from datetime import datetime

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

class ColorMatcher:
    def __init__(self):
        self.model = "gpt-4o"
        self.style_templates = self._load_style_templates()
        self.prompts = self._load_prompts()
    
    def _load_style_templates(self) -> Dict[str, Dict[str, str]]:
        """加载预定义的风格颜色模板"""
        return {
            'modern_minimalist': {
                'primary': '#FFFFFF',
                'secondary': '#333333',
                'accent': '#FF6B6B',
                'description': '现代简约风格：纯白为主，深灰点缀，红色强调'
            },
            'nordic': {
                'primary': '#F5F5F5',
                'secondary': '#B0B0B0',
                'accent': '#4A90E2',
                'description': '北欧风格：浅灰白基调，蓝色点缀'
            },
            'chinese': {
                'primary': '#F0E6D2',
                'secondary': '#8B4513',
                'accent': '#DC143C',
                'description': '中式风格：米色基调，棕色深调，红色点缀'
            },
            'industrial': {
                'primary': '#36454F',
                'secondary': '#808080',
                'accent': '#FF8C00',
                'description': '工业风格：深灰色基调，金属感，橙色强调'
            },
            'new_chinese': {
                'primary': '#E8DCC1',
                'secondary': '#8B7355',
                'accent': '#CD5C5C',
                'description': '新中式风格：暖米色，棕色，中国红'
            },
            'french': {
                'primary': '#F4E4C1',
                'secondary': '#C9A961',
                'accent': '#8B4789',
                'description': '法式风格：香槟色，金色，紫色'
            }
        }
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载 AI 提示词"""
        return {
            'analyze': '''你是一位专业的色彩设计师。
根据以下信息，生成最优的颜色搭配方案：

信息：
- 风格: {style}
- 房间类型: {room_type}
- 用户偏好: {preferences}
- 其他信息: {additional_info}

请提供以下内容（JSON格式）：
1. primary_color: 主色（HEX和RGB）
2. secondary_color: 辅色（HEX和RGB）
3. accent_color: 点缀色（HEX和RGB）
4. psychology: 色彩心理学解释
5. application: 色彩应用建议（墙面、家具、配饰等）
6. effect_description: 效果描述
7. similar_options: 2-3个相似的备选方案'''
        }
    
    def recommend_colors(self, color_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        推荐颜色搭配
        
        Args:
            color_data: 颜色数据
                - style: 风格类型
                - room_type: 房间类型
                - preferences: 用户偏好
                - reference_image: 参考图片（可选）
        
        Returns:
            Dict 包含颜色方案
        """
        try:
            logger.info(f"开始推荐颜色: {color_data.get('style')}")
            
            style = color_data.get('style', 'modern_minimalist')
            
            # 如果是预定义风格，直接返回模板
            if style in self.style_templates:
                template = self.style_templates[style]
                return {
                    'success': True,
                    'scheme_id': f"colors_{datetime.now().timestamp()}",
                    'style': style,
                    'colors': {
                        'primary': template['primary'],
                        'secondary': template['secondary'],
                        'accent': template['accent']
                    },
                    'description': template['description'],
                    'source': 'template',
                    'timestamp': datetime.now().isoformat()
                }
            
            # 否则调用 AI 生成
            prompt = self.prompts['analyze'].format(
                style=style,
                room_type=color_data.get('room_type', 'bedroom'),
                preferences=color_data.get('preferences', 'warm'),
                additional_info=color_data.get('additional_info', '')
            )
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是专业的色彩设计师。提供基于色彩理论的设计方案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            result_text = response['choices'][0]['message']['content']
            
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                result = {'raw_response': result_text, 'status': 'partial'}
            
            return {
                'success': True,
                'scheme_id': f"colors_{datetime.now().timestamp()}",
                'style': style,
                'color_scheme': result,
                'source': 'ai',
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'ai_model': self.model,
                    'tokens_used': response['usage']['total_tokens']
                }
            }
        
        except Exception as e:
            logger.error(f"颜色推荐失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# 全局实例
_color_matcher = ColorMatcher()

def recommend_colors_skill(color_data: Dict[str, Any]) -> Dict[str, Any]:
    """Skill 入口函数"""
    return _color_matcher.recommend_colors(color_data)
