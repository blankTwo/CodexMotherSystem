# UI Design System Rules

## Goal
为新建或优化 UI 提供稳定的视觉基线，避免字号失控、间距失控、首屏溢出、随机颜色和随机组件尺寸。

本规则是默认设计系统基线。若项目已有更明确的 design system、组件库或 tokens，优先遵循项目已有规范。

---

## Design Principles
- Consistency: 颜色、字号、间距、圆角、阴影、交互状态保持统一
- Hierarchy: 通过字号、字重、颜色、间距和区块权重建立信息层级
- Readability: 可读性优先于视觉装饰
- Accessibility: 默认满足 WCAG AA，正文对比度不低于 4.5:1
- Responsive: Desktop / Tablet / Mobile 均需要可用，不只适配大屏
- Viewport Fit: 单任务页面优先避免首屏无意义滚动

---

## Design Tokens

### Color
默认使用语义化 token，不直接散写随机颜色。

Primary:
- `--color-primary-50: #eef6ff`
- `--color-primary-100: #d9ebff`
- `--color-primary-500: #1677ff`
- `--color-primary-600: #0958d9`
- `--color-primary-700: #003eb3`

Neutral:
- `--color-gray-50: #fafafa`
- `--color-gray-100: #f5f5f5`
- `--color-gray-200: #e5e5e5`
- `--color-gray-300: #d4d4d4`
- `--color-gray-400: #a3a3a3`
- `--color-gray-500: #737373`
- `--color-gray-600: #525252`
- `--color-gray-700: #404040`
- `--color-gray-800: #262626`
- `--color-gray-900: #171717`

Semantic:
- `--color-success: #22c55e`
- `--color-warning: #f59e0b`
- `--color-error: #ef4444`
- `--color-info: #3b82f6`

Dark mode baseline:
- `--bg-primary: #0f1115`
- `--bg-secondary: #181a20`
- `--text-primary: #ffffff`
- `--text-secondary: #a1a1aa`

### Typography
默认字体栈：

```css
Inter, SF Pro Display, PingFang SC, Helvetica, sans-serif
```

Type scale:
- H1: `clamp(32px, 2vw, 40px)`, weight 700, line-height 1.2
- H2: `clamp(24px, 1.8vw, 32px)`, weight 700, line-height 1.3
- H3: `20-24px`, weight 600, line-height 1.4
- Body Large: `18px`, weight 400, line-height 1.7
- Body: `16px`, weight 400, line-height 1.6
- Small: `14px`, weight 400, line-height 1.5
- Caption: `12px`, weight 400, line-height 1.4

Typography guardrails:
- 品牌区、hero、登录页标题不得无判断地超过 H1 上限
- 登录页、表单页、设置页等单任务页面，首屏标题通常使用 H1/H2 范围，不使用超大展示字
- 最小字号 12px；正文默认 14-16px
- 行高必须随字号调整，不使用拥挤行高

### Spacing
使用 8pt grid。优先使用以下 spacing：
- `--space-1: 4px`
- `--space-2: 8px`
- `--space-3: 12px`
- `--space-4: 16px`
- `--space-5: 20px`
- `--space-6: 24px`
- `--space-8: 32px`
- `--space-10: 40px`
- `--space-12: 48px`
- `--space-16: 64px`

Spacing guardrails:
- 表单控件内部间距通常使用 8-16px
- 组件之间通常使用 16-24px
- 区块之间通常使用 32-48px
- 单任务首屏不要无判断使用 64px 以上大间距
- 禁止为了“高级感”堆叠过大 padding 导致 768/800/900 高度视口出现无意义滚动

### Radius
- XS: 4px
- SM: 6px
- MD: 8px
- LG: 12px
- XL: 16px
- 2XL: 24px
- Full: 9999px

### Shadow
- SM: `0 1px 2px rgba(0,0,0,0.05)`
- MD: `0 4px 12px rgba(0,0,0,0.08)`
- LG: `0 10px 30px rgba(0,0,0,0.12)`

Shadow guardrails:
- 卡片默认最多使用 `shadow-md`
- 不为每个区块都加阴影
- 阴影用于层级，不用于装饰堆叠

---

## Layout System

### Grid And Width
- 默认使用 12-column grid
- 基础单位为 8px
- 最大内容宽度不超过 1440px
- 内容区应有合理 `max-width`，避免大屏过度拉伸

### Breakpoints
- SM: 640px
- MD: 768px
- LG: 1024px
- XL: 1280px
- 2XL: 1440px

### Viewport Baseline
Desktop Web 至少检查：
- 1440x900
- 1280x800
- 1024x768

单任务页面，例如登录、注册、找回密码、简单设置页：
- 默认应在 1024x768、1280x800、1440x900 下不出现无意义纵向滚动
- 若必须滚动，滚动应由真实内容驱动，而不是由过大字号、过大 padding、装饰区或平均双栏造成
- 品牌区不得和表单区同等饱满；一侧主任务，一侧支撑

---

## Component Standards

### Button
- Small: 32px height
- Medium: 40px height
- Large: 48px height
- 最小可点击区域 44x44px
- 必须覆盖 hover / focus / pressed / disabled / loading
- transition 默认 150-200ms

### Input
- 默认高度 40px
- 默认圆角 8px
- 必须覆盖 focus / error / disabled / placeholder
- 标签、帮助文本、错误信息保持固定层级

### Card
- 默认 padding 24px
- 默认圆角 16px
- 默认最多 `shadow-md`
- 不要给所有卡片相同高度、相同边框、相同阴影

---

## Motion
- Fast: 150ms
- Normal: 200ms
- Slow: 300ms
- 动效用于状态变化、反馈和层级转换，不用于填补空洞
- Dashboard / 数据密集页面避免装饰性动画

---

## Accessibility
- 正文文字对比度 >= 4.5:1
- 大字对比度 >= 3:1
- 最小触控区域 44x44px
- 最小字号 12px
- 键盘可访问，焦点态必须可见

---

## Engineering Rules

禁止：
- 任意 magic number
- 任意颜色
- 任意阴影
- 任意圆角
- 任意超大字号
- 任意 viewport 高度假设

必须：
- 使用 design tokens 或项目已有 tokens
- 使用统一 spacing
- 使用统一 typography
- 使用统一 component API 或项目已有组件模式
- 在常见 viewport 下检查首屏是否失控

---

## Quality Checklist
- 字号是否在 type scale 内，品牌/hero 字号是否过大
- 页面是否使用 8pt spacing，而不是零散 magic number
- 单任务页面是否在 1024x768 / 1280x800 / 1440x900 下避免无意义滚动
- 卡片、按钮、输入框尺寸是否统一
- hover / focus / disabled / loading / error 状态是否完整
- 颜色、圆角、阴影是否来自 token 或项目既有模式
- 对比度、触控区域、最小字号是否达标
