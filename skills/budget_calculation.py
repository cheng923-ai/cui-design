"""
Skill 4: 预算自动化计算 (Budget Calculation)

功能：
- 计算硬装、人工、软装、家电费用
- 生成详细的预算报表
- 支持成本分析和优化
"""

import os
import json
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class BudgetCalculator:
    def __init__(self):
        self.price_database = self._load_price_database()
        self.calculation_rules = self._load_calculation_rules()
    
    def _load_price_database(self) -> Dict[str, Dict[str, float]]:
        """加载价格数据库"""
        return {
            'hard_materials': {
                'wall_paint': 50,  # 元/平方米
                'flooring_tile': 150,
                'flooring_wood': 200,
                'ceiling': 80,
                'wall_treatment': 120
            },
            'labor': {
                'painting': 30,  # 元/平方米
                'tiling': 60,
                'flooring': 50,
                'general': 40
            },
            'soft_furnishing': {
                'sofa_low': 2000,
                'sofa_medium': 5000,
                'sofa_high': 10000,
                'curtain': 500,
                'carpet': 2000
            },
            'appliances': {
                'ac': 3000,
                'heater': 2000,
                'lighting': 1000,
                'ventilation': 1500
            }
        }
    
    def _load_calculation_rules(self) -> Dict[str, Any]:
        """加载计算规则"""
        return {
            'tax_rate': 0.13,  # 增值税
            'profit_margin': 0.15,  # 利润率
            'contingency': 0.1  # 预留金（10%）
        }
    
    def calculate_budget(self, budget_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算项目预算
        
        Args:
            budget_data: 预算数据
                - area: 面积
                - room_type: 房间类型
                - style: 设计风格
                - hard_materials: 硬装材料清单
                - soft_furnishings: 软装清单
                - appliances: 家电清单
        
        Returns:
            Dict 包含预算明细
        """
        try:
            logger.info("开始计算预算")
            
            area = budget_data.get('area', 100)
            
            # 计算硬装费用
            hard_cost = self._calculate_hard_materials(budget_data, area)
            
            # 计算人工费用
            labor_cost = self._calculate_labor(budget_data, area)
            
            # 计算软装费用
            soft_cost = self._calculate_soft_furnishing(budget_data)
            
            # 计算家电费用
            appliance_cost = self._calculate_appliances(budget_data)
            
            # 汇总
            subtotal = hard_cost + labor_cost + soft_cost + appliance_cost
            
            # 添加税费和利润
            tax = subtotal * self.calculation_rules['tax_rate']
            profit = subtotal * self.calculation_rules['profit_margin']
            contingency = subtotal * self.calculation_rules['contingency']
            
            total = subtotal + tax + profit + contingency
            
            return {
                'success': True,
                'budget_id': f"budget_{datetime.now().timestamp()}",
                'area': area,
                'breakdown': {
                    'hard_materials': {
                        'amount': hard_cost,
                        'percentage': hard_cost / subtotal * 100 if subtotal > 0 else 0,
                        'description': '墙面、地面、天花等基础装修'
                    },
                    'labor': {
                        'amount': labor_cost,
                        'percentage': labor_cost / subtotal * 100 if subtotal > 0 else 0,
                        'description': '施工人工费'
                    },
                    'soft_furnishing': {
                        'amount': soft_cost,
                        'percentage': soft_cost / subtotal * 100 if subtotal > 0 else 0,
                        'description': '沙发、窗帘、地毯等软装'
                    },
                    'appliances': {
                        'amount': appliance_cost,
                        'percentage': appliance_cost / subtotal * 100 if subtotal > 0 else 0,
                        'description': '空调、照明等家电'
                    }
                },
                'costs': {
                    'subtotal': round(subtotal, 2),
                    'tax': round(tax, 2),
                    'profit': round(profit, 2),
                    'contingency': round(contingency, 2),
                    'total': round(total, 2)
                },
                'unit_price': round(total / area, 2) if area > 0 else 0,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"预算计算失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_hard_materials(self, budget_data: Dict[str, Any], area: float) -> float:
        """计算硬装费用"""
        cost = 0
        materials = budget_data.get('hard_materials', {})
        db = self.price_database['hard_materials']
        
        for material, quantity in materials.items():
            if material in db:
                cost += db[material] * quantity
        
        # 如果没有指定，使用默认值
        if not materials:
            cost = area * 800  # 默认每平方米 800 元
        
        return cost
    
    def _calculate_labor(self, budget_data: Dict[str, Any], area: float) -> float:
        """计算人工费用"""
        labor = budget_data.get('labor_cost')
        if labor:
            return labor
        return area * 400  # 默认每平方米 400 元
    
    def _calculate_soft_furnishing(self, budget_data: Dict[str, Any]) -> float:
        """计算软装费用"""
        cost = 0
        items = budget_data.get('soft_furnishings', {})
        
        for item, price in items.items():
            cost += price
        
        return cost
    
    def _calculate_appliances(self, budget_data: Dict[str, Any]) -> float:
        """计算家电费用"""
        cost = 0
        items = budget_data.get('appliances', {})
        
        for item, price in items.items():
            cost += price
        
        return cost

# 全局实例
_calculator = BudgetCalculator()

def calculate_budget_skill(budget_data: Dict[str, Any]) -> Dict[str, Any]:
    """Skill 入口函数"""
    return _calculator.calculate_budget(budget_data)
