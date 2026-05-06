# UI Consistency Rules

## Goal
所有新增或修改的页面，必须优先保持与项目现有 UI 风格一致，而不是凭空设计。

## Mandatory Checks
开始实现 UI 前，必须先检查：
1. 是否已有项目 design system / tokens / 组件库规范
2. 若无项目规范，先使用 `rules/ui-design-system.md` 的默认基线
3. 项目中相似页面的布局方式
4. 已存在的组件库/基础组件
5. 常用 Tailwind 写法
6. 常用间距、字号、圆角、颜色、按钮风格
7. 表格、表单、弹窗、卡片的已有模式
8. 常见 viewport 下是否会出现首屏失控或无意义滚动

## Component Priority
实现 UI 时，优先级如下：
1. 项目已有业务组件
2. 项目已有基础组件
3. 组件库组件
4. 原生 HTML 标签

禁止在明明已有对应组件的情况下，直接退回原生 HTML 拼装整页 UI。

## Tailwind Rules
- 优先使用项目中已有的 Tailwind 写法
- 优先使用语义化、统一化 class
- 优先使用 design token 对应的 Tailwind 档位
- 非必要禁止使用任意值，如：
  - `text-[12px]`
  - `mt-[7px]`
  - `rounded-[3px]`

## Preferred Mapping
若项目已有统一写法，则优先遵循，例如：
- `text-xs` 优先于 `text-[12px]`
- `rounded-md` 优先于 `rounded-[6px]`
- `px-3 py-2` 优先于碎片化任意值
- `gap-2 / gap-3 / gap-4` 优先于 `gap-[10px]`

## UI Optimization Means
当用户要求“优化 UI”时，默认包含：
1. 与现有页面风格统一
2. 提升层级与间距一致性
3. 提升可读性
4. 提升交互态完整性
5. 减少无意义 class 和结构嵌套
6. 优先复用组件，而不是重写
7. 检查字号、spacing、组件尺寸和首屏 viewport 是否符合 `rules/ui-design-system.md`

## Forbidden
- 不参考现有页面直接重新发明风格
- 随意使用任意值破坏统一性
- 无判断使用超大字号、超大 padding 或随机色值
- 让登录、注册、简单设置等单任务页面因为装饰或比例失衡出现无意义滚动
- 把所有样式直接堆到单个 JSX 节点
- 在已有组件库前提下大量手写原生控件外观
