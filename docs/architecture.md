# CUI-Design 系统架构文档

## 1. 整体架构设计

### 1.1 三层架构

```
┌────────────────────────────────────────────────────────┐
│                    表现层 (Presentation)                 │
│  Web App (React/Vue) | CAD Plugin | 3D Max Plugin      │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│                  业务逻辑层 (Business Logic)           │
│  Python Backend (Flask/FastAPI)                        │
│  - AI Skills 处理                                      │
│  - 数据处理和转换                                      │
│  - 规则引擎                                            │
└────────────────────┬─────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────┐
│                   数据层 (Data Layer)                   │
│  Database | File Storage | AI Model APIs               │
└────────────────────────────────────────────────────────┘
```

### 1.2 组件交互流程

```
用户输入
  │
  ▼
┌─────────────────┐
│   Web 应用/插件  │ (输入户型、参数、风格等)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Python 后端API  │ (处理请求)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  AI Skills 处理链                    │
│  ┌──────────────────────────────┐   │
│  │ 1. 空间布局优化              │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ 2. 颜色搭配推荐              │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ 3. 软装搭配推荐              │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ 4. 预算计算                  │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ 5. 施工图生成                │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ 6. 效果图渲染                │   │
│  └──────────────────────────────┘   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  结果输出       │ (数据、图片、报表)
└─────────────────┘
```

## 2. 各 Skill 模块的工作流

### 2.1 空间布局优化 (Space Layout Optimization)

**输入**:
- 户型平面图（图片或 CAD 文件）
- 或房间参数：长、宽、高、房间用途、窗户位置等

**处理流程**:
```
输入房间信息
    ↓
图像识别（如果是图片）
    ↓
提取房间特征（面积、采光点、障碍物）
    ↓
AI 分析最优布局
    ↓
生成多个布局方案
    ↓
评分排序
    ↓
输出推荐方案
```

**输出**:
- 家具摆放推荐位置
- 动线流线优化
- 功能区划分
- 采光通风建议
- 标注平面图
- 3D 示意图

**关键 AI 提示词**:
```
分析这个{room_type}房间：
- 尺寸: {length}m × {width}m × {height}m
- 窗户位置: {window_position}
- 用途: {purpose}

请提供：
1. 最优家具摆放方案
2. 动线流线分析
3. 功能区划分建议
4. 采光和通风优化
5. 平面图标注
```

---

### 2.2 颜色搭配推荐 (Color Matching)

**输入方式**:
1. 选择风格模板
2. 输入风格描述
3. 上传参考图片

**处理流程**:
```
获取风格信息
    ↓
风格识别/匹配
    ↓
颜色心理学分析
    ↓
生成主色/辅色/点缀色方案
    ↓
按房间类型调整
    ↓
生成 HEX/RGB 色值
    ↓
生成效果预览
```

**输出**:
- 主色（60%）、辅色（30%）、点缀色（10%）
- HEX 和 RGB 色值
- 色彩心理学解释
- 应用区域建议
- 效果图预览

**支持的风格模板**:
- 现代简约 (Modern Minimalist)
- 北欧 (Nordic)
- 中式 (Chinese)
- 工业风 (Industrial)
- 新中式 (New Chinese)
- 法式 (French)
- 地中海 (Mediterranean)
- 日式 (Japanese)
- 美式 (American)

---

### 2.3 软装搭配推荐 (Furniture Recommendation)

**输入**:
- 房间类型、面积、风格、预算
- 客户生活方式偏好

**处理流程**:
```
获取房间和预算信息
    ↓
检索产品数据库
    ↓
根据预算档位筛选
    ↓
根据风格和功能推荐
    ↓
考虑尺寸匹配
    ↓
生成搭配清单
    ↓
获取产品和链接
    ↓
输出效果图
```

**输出**:
- 软装物品清单（沙发、窗帘、地毯、装饰画等）
- 产品推荐（品牌+型号+价格）
- 采购链接和渠道
- 搭配效果图

**预算档位**:
- 低端 (Low): 基础款，性价比高
- 中端 (Medium): 品质和设计的平衡
- 高端 (High): 高品质设计品牌

---

### 2.4 预算自动化计算 (Budget Calculation)

**输入**:
- 房间信息（面积、用途）
- 选定的材料和家具
- 施工工艺

**处理流程**:
```
获取项目详情
    ↓
计算各项成本：
  - 硬装材料 = 面积 × 单价
  - 人工费 = 工日 × 时薪
  - 软装 = 选定产品总价
  - 家电 = 选定产品总价
    ↓
汇总成本
    ↓
添加税费和利润
    ↓
生成明细报表
    ↓
生成预算分配图表
```

**输出**:
- 总预算金额
- 分项目明细：
  - 硬装材料费
  - 人工费
  - 软装物品费
  - 家电费
  - 其他费用
- 单价×数量清单
- 预算分配饼图
- 可导出的预算表格

---

### 2.5 施工图自动化生成 (Construction Drawing)

**输入**:
- 空间布局方案
- 颜色搭配方案
- 施工工艺信息

**处理流程**:
```
获取设计方案
    ↓
生成平面布置图
    ↓
生成顶面布置图
    ↓
生成立面图
    ↓
生成详图和节点图
    ↓
添加材料说明
    ↓
生成尺寸标注
    ↓
输出 CAD/PDF 文件
```

**输出**:
- A4 规格施工图集
- 包含：平面、顶面、立面、详图
- 材料规格和做法说明
- CAD 格式（支持进一步编辑）

---

### 2.6 效果图自动化生成 (Rendering)

**输入**:
- 所有前期设计方案
- 渲染参数（光照、视角等）

**处理流程**:
```
整合所有设计信息
    ↓
生成 3D 场景数据
    ↓
调用 AI 渲染模型（DALL-E/Stable Diffusion）
    ↓
生成多个视角
    ↓
日景和夜景渲染
    ↓
后处理和优化
    ↓
输出高清效果图
```

**输出**:
- 2D 平面效果图（俯视图）
- 3D 立体效果图（多角度）
- 日景效果图
- 夜景效果图

---

## 3. 数据流设计

### 3.1 核心数据模型

```
Project
├── id: UUID
├── name: string
├── description: string
├── created_at: datetime
├── updated_at: datetime
│
├── FloorPlan
│   ├── room_id
│   ├── image_url
│   ├── dimensions
│   └── extracted_features
│
├── SpaceLayout
│   ├── furniture_placement
│   ├── flow_analysis
│   ├── zoning
│   └── recommendations
│
├── ColorScheme
│   ├── primary_color (HEX)
│   ├── secondary_color (HEX)
│   ├── accent_color (HEX)
│   ├── style
│   └── psychology
│
├── FurnitureRecommendation
│   ├── items[]
│   │   ├── name
│   │   ├── brand
│   │   ├── model
│   │   ├── price
│   │   └── link
│   └── total_price
│
├── Budget
│   ├── line_items[]
│   │   ├── category
│   │   ├── description
│   │   ├── unit_price
│   │   ├── quantity
│   │   └── subtotal
│   └── total
│
├── ConstructionDrawing
│   ├── floor_plan_url
│   ├── ceiling_plan_url
│   ├── elevation_urls[]
│   ├── detail_urls[]
│   └── materials_doc_url
│
└── Rendering
    ├── front_view_url
    ├── side_view_url
    ├── top_view_url
    ├── day_lighting_url
    └── night_lighting_url
```

## 4. API 架构

### 4.1 RESTful 端点设计

```
POST   /api/projects                    # 创建新项目
GET    /api/projects/{id}              # 获取项目详情
PUT    /api/projects/{id}              # 更新项目

POST   /api/projects/{id}/layout       # 优化空间布局
GET    /api/projects/{id}/layout       # 获取布局结果

POST   /api/projects/{id}/colors       # 生成颜色方案
GET    /api/projects/{id}/colors       # 获取颜色方案

POST   /api/projects/{id}/furniture    # 推荐软装
GET    /api/projects/{id}/furniture    # 获取软装清单

POST   /api/projects/{id}/budget       # 计算预算
GET    /api/projects/{id}/budget       # 获取预算报表

POST   /api/projects/{id}/construction # 生成施工图
GET    /api/projects/{id}/construction # 获取施工图

POST   /api/projects/{id}/rendering    # 生成效果图
GET    /api/projects/{id}/rendering    # 获取效果图
```

## 5. 部署架构

### 5.1 开发环境

```
Developer Machine
├── Frontend (npm start)
├── Backend (python app.py)
├── Plugins (CAD/3D Max)
└── Database (SQLite)
```

### 5.2 生产环境

```
Cloud Server (AWS/Aliyun/etc)
├── Frontend (React Build + Nginx)
├── Backend (Gunicorn + Python)
├── Database (PostgreSQL)
├── File Storage (S3/OSS)
└── AI Model APIs (OpenAI/Claude)
```

## 6. 安全和性能考虑

### 6.1 安全性
- API 认证和授权（JWT）
- 输入验证和清理
- 敏感信息加密存储
- HTTPS 传输

### 6.2 性能优化
- 异步任务处理（Celery）
- 缓存策略（Redis）
- 数据库查询优化
- CDN 加速

---

**最后更新**: 2024年
