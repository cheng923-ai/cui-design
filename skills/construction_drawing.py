"""
Skill 5: 施工图自动化生成 (Construction Drawing)

功能：
- 基于设计方案生成施工图
- 包含平面、立面、顶面等
- 添加尺寸和材料说明
"""

import os
import json
import logging
from typing import Dict, List, Any
import openai
from datetime import datetime

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

class ConstructionDrawingGenerator:
    def __init__(self):
        self.model = "gpt-4o"
        self.drawing_templates = self._load_drawing_templates()
        self.prompts = self._load_prompts()
    
    def _load_drawing_templates(self) -> Dict[str, Dict[str, str]]:
        """加载施工图模板"""
        return {
            'floor_plan': '平面布置图模板',
            'ceiling_plan': '顶面布置图模板',
            'elevation': '立面图模板',
            'detail': '详图模板'
        }
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载 AI 提示词"""
        return {
            'generate': '''你是一位专业的施工图设计师。
基于以下设计方案，生成详细的施工图说明：

设计信息：
- 房间类型: {room_type}
- 尺寸: {dimensions}
- 风格: {style}
- 材料规格: {materials}
- 工艺要求: {construction_methods}

请提供以下内容（JSON格式）：
1. floor_plan: 平面布置图说明
2. ceiling_plan: 顶面布置图说明
3. elevation: 立面图说明
4. details: 详图和节点说明
5. materials: 材料规格清单
6. dimensions: 尺寸标注说明
7. construction_notes: 施工说明和工艺要求'''
        }
    
    def generate_construction_drawing(self, drawing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成施工图
        
        Args:
            drawing_data: 施工图数据
                - layout_id: 布局方案 ID
                - color_id: 颜色方案 ID
                - materials: 材料清单
                - construction_methods: 施工工艺
        
        Returns:
            Dict 包含施工图信息
        """
        try:
            logger.info("开始生成施工图")
            
            prompt = self.prompts['generate'].format(
                room_type=drawing_data.get('room_type', 'living_room'),
                dimensions=drawing_data.get('dimensions', '5m x 4m x 2.8m'),
                style=drawing_data.get('style', 'modern'),
                materials=json.dumps(drawing_data.get('materials', [])),
                construction_methods=json.dumps(drawing_data.get('construction_methods', []))
            )
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是专业的施工图设计师。生成详细、规范的施工图。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2500
            )
            
            result_text = response['choices'][0]['message']['content']
            
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                result = {'raw_response': result_text, 'status': 'partial'}
            
            return {
                'success': True,
                'drawing_id': f"drawing_{datetime.now().timestamp()}",
                'drawing_set': result,
                'file_format': 'CAD/PDF',
                'includes': [
                    'floor_plan',
                    'ceiling_plan',
                    'elevation',
                    'details'
                ],
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'ai_model': self.model,
                    'tokens_used': response['usage']['total_tokens']
                }
            }
        
        except Exception as e:
            logger.error(f"施工图生成失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# 全局实例
_generator = ConstructionDrawingGenerator()

def generate_construction_drawing_skill(drawing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Skill 入口函数"""
    return _generator.generate_construction_drawing(drawing_data)
