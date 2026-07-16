# CUI-Design: AI-Powered Residential Interior Design Automation Skills

**CUI-Design** 是一套完整的 AI 驱动的住宅室内设计自动化系统，旨在提升设计师的工作效率，自动化设计决策过程。

## 核心功能模块

### 1. 🏗️ 空间布局优化建议 (Space Layout Optimization)
- **输入**: 户型平面图或房间参数（长×宽×高、房间用途、窗户位置）
- **输出**:
  - 家具摆放位置推荐
  - 动线流线优化建议
  - 功能区划分方案
  - 采光和通风建议
  - 标注后的平面图
  - 3D 示意图

### 2. 🎨 颜色搭配推荐 (Color Matching Recommendation)
- **输入方式**:
  - 选择预定义风格模板（现代简约、北欧、中式、工业风、新中式、法式、地中海等）
  - 手动输入风格描述
  - 上传参考图片进行 AI 识别
- **输出**:
  - 主色、辅色、点缀色的 HEX/RGB 色值
  - 色彩心理学解释
  - 色彩应用区域建议（墙面、家具、配饰等）
  - 色彩搭配效果图预览
  - 支持按房间类型差异化推荐

### 3. 🛋️ 软装搭配推荐 (Soft Furnishing Recommendation)
- **输入信息**:
  - 房间类型（卧室、客厅、书房等）
  - 房间面积
  - 风格偏好
  - 预算范围
  - 客户生活方式和偏好
- **输出**:
  - 软装物品清单（沙发、窗帘、地毯、装饰画等）
  - 具体产品推荐（品牌+型号）
  - 价格区间
  - 采购链接和渠道建议
  - 软装搭配效果图

### 4. 📊 预算自动化计算 (Budget Automation)
- **包含项目**:
  - 硬装材料费（墙面、地面、天花板等）
  - 人工费
  - 软装物品费
  - 家电费
  - 其他费用
- **输出形式**:
  - 总预算金额
  - 分项目明细表
  - 单价×数量详细清单
  - 可视化的预算分配图表

### 5. 📐 施工图自动化生成 (Construction Drawing Automation)
- **生成内容**:
  - 平面布置图
  - 顶面布置图
  - 立面图
  - 详图和节点图
  - 材料说明
- **基于**:
  - 空间布局优化结果
  - 颜色搭配方案
  - 施工工艺信息

### 6. 🖼️ 效果图自动化生成 (Rendering Automation)
- **触发方式**:
  - 完成空间布局、颜色搭配、软装搭配后一键生成
  - 随时生成单个房间效果图
- **输出内容**:
  - 2D 平面图效果（俯视图）
  - 3D 立体效果图（类似 3D Max 渲染）
  - 多角度视图
  - 日景和夜景
  - 高保真渲染质量

## 系统架构

```
┌─────────────────────────────────────────────────┐
│         Web 应用（React/Vue）- 前端大脑         │
│  - 户型上传/参数输入                              │
│  - 风格选择/参考图片                              │
│  - 实时预览                                       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│    Python 脚本 (Flask/FastAPI) - 中间枢纽      │
│  - 数据处理和转换                                 │
│  - AI 模型调用                                   │
│  - CAD/3D Max 接口                              │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│ CAD 插件         │  │ 3D Max 插件      │
│ - 导入户型图     │  │ - 导入户型图     │
│ - 导出结果       │  │ - 导出结果       │
└──────────────────┘  └──────────────────┘
```

## 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | React / Vue.js |
| **后端** | Python (Flask/FastAPI) |
| **AI 模型** | OpenAI GPT-4o / Claude / Gemini |
| **CAD 插件** | CAD.NET API |
| **3D Max 插件** | MAXScript |
| **数据库** | SQLite (本地) / PostgreSQL (云端) |
| **效果图生成** | DALL-E / Stable Diffusion |

## 项目结构

```
cui-design/
├── README.md
├── docs/                          # 文档
│   ├── architecture.md            # 系统架构文档
│   ├── api-specification.md       # API 规范
│   ├── user-guide.md              # 用户使用指南
│   └── developer-guide.md         # 开发者指南
├── skills/                        # 核心 Skills 模块
│   ├── space-layout-optimization/
│   │   ├── README.md
│   │   ├── prompts/
│   │   ├── models/
│   │   └── scripts/
│   ├── color-matching/
│   │   ├── README.md
│   │   ├── prompts/
│   │   ├── models/
│   │   └── scripts/
│   ├── furniture-recommendation/
│   │   ├── README.md
│   │   ├── prompts/
│   │   ├── databases/
│   │   └── scripts/
│   ├── budget-calculation/
│   │   ├── README.md
│   │   ├── templates/
│   │   ├── models/
│   │   └── scripts/
│   ├── construction-drawing/
│   │   ├── README.md
│   │   ├── templates/
│   │   └── scripts/
│   └── rendering-automation/
│       ├── README.md
│       ├── prompts/
│       └── scripts/
├── backend/                       # 后端服务
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── api/
│   ├── models/
│   ├── utils/
│   └── services/
├── frontend/                      # 前端应用
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── plugins/                       # CAD/3D Max 插件
│   ├── cad-plugin/
│   ├── 3dsmax-plugin/
│   └── README.md
├── tests/                         # 测试
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── examples/                      # 使用示例
│   ├── sample-floorplans/
│   ├── sample-results/
│   └── tutorials/
└── .github/
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

## 快速开始

### 前提条件
- Python 3.9+
- Node.js 16+
- OpenAI API Key (GPT-4o)
- Git

### 安装

1. **克隆仓库**
```bash
git clone https://github.com/cheng923-ai/cui-design.git
cd cui-design
```

2. **后端配置**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，添加 OpenAI API Key
python app.py
```

3. **前端配置**
```bash
cd frontend
npm install
npm start
```

4. **插件安装**
- CAD 插件: 参考 `plugins/cad-plugin/README.md`
- 3D Max 插件: 参考 `plugins/3dsmax-plugin/README.md`

## 使用示例

### 1. 空间布局优化
```python
from skills.space_layout_optimization import optimize_layout

result = optimize_layout(
    floorplan="path/to/floorplan.jpg",
    room_params={
        "length": 5.0,
        "width": 4.0,
        "height": 2.8,
        "room_type": "living_room",
        "window_position": "south"
    }
)
```

### 2. 颜色搭配推荐
```python
from skills.color_matching import recommend_colors

colors = recommend_colors(
    style="modern_minimalist",
    room_type="bedroom",
    reference_image="path/to/reference.jpg"
)
```

### 3. 软装搭配推荐
```python
from skills.furniture_recommendation import recommend_furniture

furniture = recommend_furniture(
    room_type="living_room",
    area=30,
    style="nordic",
    budget_range="medium",
    preferences=["reading", "entertainment"]
)
```

## API 文档

详见 `docs/api-specification.md`

## 贡献指南

欢迎提交 Issues 和 Pull Requests！

## 许可证

MIT License

## 联系方式

- GitHub Issues: [CUI-Design Issues](https://github.com/cheng923-ai/cui-design/issues)
- 邮箱: your-email@example.com

---

**最后更新**: 2024年
**版本**: 0.1.0 (开发中)
