"""
Skill 3: 软装搭配推荐 (Furniture Recommendation)

功能：
- 根据房间类型和风格推荐软装
- 提供产品清单和采购链接
- 考虑预算和尺寸匹配
"""

import os
import json
import logging
from typing import Dict, List, Any
import openai
from datetime import datetime

logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

class FurnitureRecommender:
    def __init__(self):
        self.model = "gpt-4o"
        self.product_database = self._load_product_database()
        self.prompts = self._load_prompts()
    
    def _load_product_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """加载产品数据库（示例）"""
        return {
            'sofa': [
                {'name': '简约布艺沙发', 'brand': '宜家', 'price': 3999, 'style': 'modern', 'size': '200x90'},
                {'name': '北欧棉麻沙发', 'brand': '网易严选', 'price': 4999, 'style': 'nordic', 'size': '220x100'},
            ],
            'curtain': [
                {'name': '遮光窗帘', 'brand': '宜家', 'price': 199, 'style': 'modern'},
                {'name': '亚麻窗帘', 'brand': '网易严选', 'price': 299, 'style': 'nordic'},
            ],
            'carpet': [
                {'name': '羊毛地毯', 'brand': '地毯品牌', 'price': 2999, 'style': 'nordic'},
            ]
        }
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载 AI 提示词"""
        return {
            'recommend': '''你是一位专业的软装设计师。
根据以下信息，推荐合适的软装搭配：

房间信息：
- 房间类型: {room_type}
- 面积: {area}平方米
- 风格: {style}
- 预算档位: {budget_range}
- 用户偏好: {preferences}

请提供以下内容（JSON格式）：
1. recommended_items: 推荐的软装物品列表
   - 沙发/床
   - 窗帘
   - 地毯
   - 装饰画
   - 灯具
   - 其他配饰
2. total_budget: 预计总预算
3. brand_suggestions: 品牌推荐
4. shopping_tips: 采购建议
5. effect_description: 搭配效果描述'''
        }
    
    def recommend_furniture(self, furniture_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        推荐软装搭配
        
        Args:
            furniture_data: 家具数据
                - room_type: 房间类型
                - area: 面积
                - style: 风格
                - budget_range: 预算档位
                - preferences: 用户偏好
        
        Returns:
            Dict 包含家具推荐
        """
        try:
            logger.info(f"开始推荐软装: {furniture_data.get('room_type')}")
            
            prompt = self.prompts['recommend'].format(
                room_type=furniture_data.get('room_type', 'living_room'),
                area=furniture_data.get('area', 30),
                style=furniture_data.get('style', 'modern'),
                budget_range=furniture_data.get('budget_range', 'medium'),
                preferences=json.dumps(furniture_data.get('preferences', []))
            )
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是专业的软装设计师。提供实用的软装搭配方案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result_text = response['choices'][0]['message']['content']
            
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                result = {'raw_response': result_text, 'status': 'partial'}
            
            return {
                'success': True,
                'recommendation_id': f"furniture_{datetime.now().timestamp()}",
                'room_type': furniture_data.get('room_type'),
                'recommendations': result,
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'ai_model': self.model,
                    'tokens_used': response['usage']['total_tokens']
                }
            }
        
        except Exception as e:
            logger.error(f"软装推荐失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# 全局实例
_recommender = FurnitureRecommender()

def recommend_furniture_skill(furniture_data: Dict[str, Any]) -> Dict[str, Any]:
    """Skill 入口函数"""
    return _recommender.recommend_furniture(furniture_data)
