---
name: feature-ui
description: 用于从 0 到 1 生成功能级或页面级产品 UI，适用于新建页面、新建列表/表单/详情/dashboard、搭建新项目初始界面、为现有功能补充完整 UI 结构等场景。该 skill 通过跨框架的质量清单约束页面结构、状态覆盖、交互完整性、平台适配与一致性要求，但不绑定 React、Vue、Taro 等具体框架语法，也不规定组件库、状态库或样式方案。
---

# Goal
生成功能级或页面级产品 UI，并保证基础质量稳定：
- 结构清晰
- 状态完整
- 交互合理
- 平台适配
- 风格一致
- 不呈现明显 AI 模板感

# Scope
本 skill 处理的是产品 UI 的生成策略，而不是具体框架实现。

适合处理：
- 新建列表页、表单页、详情页、dashboard、设置页等产品页面
- 为新项目提供第一版可扩展 UI 骨架
- 为现有功能补齐完整的页面结构与状态设计
- 在缺少明确参考页面时，生成成熟且可落地的产品 UI

不负责处理：
- React / Vue / Taro 的具体语法实现
- hooks、composition API、store、router 等框架模式
- 组件库或样式技术选型
- 创意型品牌页、活动页、艺术化 landing page
- 领域特化的复杂可视化、编辑器、3D 或重专业交互界面

# Use With Other Skills
- 若任务明确要求 React / Vue / Taro 实现，与对应框架 skill 组合使用
- 若任务是优化已有页面，而不是新建 UI，优先使用 `ui-refine`
- 若需要在生成功能 UI 后继续打磨观感，可在生成后补用 `ui-refine`

# Workflow
1. 判断目标是新建页面、补齐功能 UI，还是只是优化已有页面
2. 判断目标平台：
   - Desktop Web
   - Mobile App
   - Mini Program / Touch Device
3. 判断交互意图：
   - 数据展示
   - 数据输入
   - 导航与流程
   - 反馈与状态
   - 内容组织
4. 查找项目中是否已有相似页面或稳定模式
5. 若存在相似页面，优先对齐其布局、层级、组件复用方式和视觉节奏
6. 若不存在相似页面，生成一版成熟、克制、产品化的默认结构
7. 按质量清单检查并补齐缺失项
8. 输出可继续实现的 UI 结构，而不是只给规划说明

# Quality Checklist

## Structure
- 页面必须有清晰区块，而不是原生标签平铺
- 主内容区、辅助区、操作区、反馈区主次明确
- 避免所有模块同层级、同权重、同节奏

## State Coverage
- 显式考虑 `loading / empty / error / success / disabled`
- 涉及提交、删除、筛选、保存、切换时，要有过程态和结果态
- 不只覆盖理想成功路径

## Interaction Completeness
- 关键操作必须有可见反馈
- 交互区域应具备合理的 hover / focus / pressed / submitting 等状态
- 避免只有静态布局而缺少真实交互闭环

## Platform Fit
- Web、App、Mini Program 应按平台习惯调整布局密度、点击区和反馈方式
- 不直接把桌面后台结构照搬到移动端
- 考虑触摸场景、滚动场景和弱网络场景

## Componentization
- 优先组织成可复用结构单元，而不是整页散写
- 即使没有现成组件库，也应保持组件化思维
- 结构复用优先于样式堆砌

## Consistency
- 字号、间距、圆角、边框、阴影、按钮风格应稳定收敛
- 同类区域保持一致写法，不要每块单独发明视觉规则
- 新项目也要建立稳定视觉档位

## Anti-AI Signals
- 避免所有卡片、区块、信息层级完全一样
- 避免“标题 + 内容 + 按钮”重复堆叠的模板布局
- 避免大量原生控件直接拼接形成廉价感
- 避免依赖零碎 arbitrary values 拼出表面精致感

## Output Standard
- 最终输出必须能继续落地实现，而不是停留在概念和规划
- 若已有项目上下文，优先贴近现有风格
- 若缺少上下文，也要输出成熟、可扩展的默认结构

# Output
- 页面或功能 UI 的结构说明
- 关键区块与组件组织方式
- 状态覆盖说明
- 平台适配要点
- 需要框架 skill 承接的实现边界

# Handoff to Implementation Skills
当需要交给 `feature-react` 或其他实现 skill 时，至少应交接以下内容：
- 页面结构：页面由哪些区块组成，主次关系如何
- 组件边界：哪些区域应独立成组件，哪些保持在页面内
- 状态设计：需要覆盖哪些 `loading / empty / error / success / disabled` 状态
- 交互流程：关键操作的触发、处理、反馈路径
- 平台差异：当前平台下需要特别处理的布局、触控、滚动或反馈点
- 实现边界：哪些部分已经由本 skill 决定，哪些部分留给框架 skill 落地

禁止只交付纯概念说明而没有可继续实现的结构信息。

# Memory Usage
- 若形成项目级 UI 结构模式，写入 `memory/projects/{project}.md`
- 若形成跨项目稳定可复用的质量检查模式，提议升级到 `memory/global/reusable-patterns.md` 或对应 rules
