---
name: feature-react
description: 用于在 React 项目中实现页面、组件、交互、状态逻辑和请求流程，适用于新增 React 页面、补充 React 交互、拆分 component/hook/store/api、承接 `feature-ui` 生成的页面结构并落地为 React 代码等场景。该 skill 负责 React 语法与实现模式，不负责跨框架的通用 UI 生成策略。
---

# Goal
以符合 React 项目习惯的方式实现页面和功能，包括：
- 组件拆分
- hooks 使用
- 状态组织
- 请求流程接入
- 事件与交互实现

该 skill 关注“如何在 React 中实现”，而不是“页面应该长什么样”。

# Scope
适合处理：
- 新增 React 页面并落地为具体组件代码
- 新增 React 组件、交互与页面逻辑
- 识别代码应放在 component / hook / store / api 的位置
- 实现查询、提交、局部状态与副作用逻辑
- 承接 `feature-ui` 产出的页面结构并转为 React 代码

不负责处理：
- 跨框架通用 UI 生成策略
- “去 AI 感”、统一风格、页面观感优化
- 脱离 React 上下文的纯视觉结构设计
- 组件库或设计系统本体的定义

# Use With Other Skills
- 若任务是从 0 到 1 新建页面 UI，先使用 `feature-ui`，再用本 skill 落地 React 实现
- 若任务是优化已有页面观感和一致性，优先使用 `ui-refine`
- 若任务既有新页面 UI 又有 React 实现，组合使用 `feature-ui` + `feature-react`

# Input from feature-ui
若承接 `feature-ui` 的输出，先检查以下内容是否明确：
- 页面结构是否清晰，主区块与次区块是否已定义
- 组件边界是否明确，哪些部分应拆成组件是否可判断
- 状态覆盖是否完整，至少包含关键的加载、空态、错误和成功反馈
- 交互流程是否明确，关键操作的触发与反馈是否可实现
- 平台适配点是否已标出，是否需要针对当前平台补充处理

若以上信息缺失，不要直接进入 React 代码实现；先补齐结构和交互定义，再继续落地。

# Steps
1. 明确功能目标
2. 明确 UI、状态、数据来源
3. 识别应放在 component / hook / store / api 的位置
4. 优先复用已有模式
5. 按层实现
6. 处理加载、错误、空态
7. 验证主流程与关键边界
8. 将项目特有模式写入 project memory

# Output
- 功能拆分
- React 组件与 hooks 组织方式
- 关键状态流
- 影响文件
- 验证建议
