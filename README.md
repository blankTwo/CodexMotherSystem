# Codex Mother System v2

一个面向前端产品开发的 Codex 母体系统。

它的目标不是为每个项目重复搭建一套 AGENTS / rules / skills，而是用一套可复用母体服务多个项目，同时通过项目记忆保持上下文隔离。

## 这是什么

这套系统主要解决 4 件事：

- 用统一入口管理不同项目的执行规则
- 把重复经验从项目记忆沉淀成 skill，再升级为 rule
- 让 UI、React、测试、重构等流程可以跨项目复用
- 避免不同项目之间的业务细节互相污染

它更适合：

- 前端产品开发项目
- React 为主、未来可能扩展 Vue / Taro 的团队
- 希望长期沉淀可复用规则与技能的场景

## 快速开始

### 第一次使用

1. 保持本目录中的 `AGENTS.md`、`rules/`、`skills/`、`memory/` 完整存在
2. 在任意项目中复用这套母体系统
3. 由 `AGENTS.md` 负责识别项目、技术栈、匹配 rules 和 skills
4. 将项目特定经验写入 `memory/projects/{project}.md`

### 典型工作流

**场景 1：修复一个 React 项目 bug**

- 系统识别技术栈为 React
- 读取 `rules/frontend-react.md`
- 选择 `skills/bugfix/`
- 修复后把项目特定坑点写入对应 project memory

**场景 2：从 0 到 1 新建一个产品页面**

- 系统识别这是 UI 新建任务
- 读取 `rules/ui-consistency.md`
- 选择 `skills/feature-ui/`
- 如果项目是 React，再叠加 `skills/feature-react/`

**场景 3：优化已有页面**

- 系统识别这是 UI 优化任务
- 读取 `rules/ui-consistency.md`
- 选择 `skills/ui-refine/`
- 重点统一风格、减少原生拼装感、提升成熟度

## 核心概念

### AGENTS / rules / skills / memory 的关系

| 层级 | 作用 | 适合放什么 | 更新频率 |
| --- | --- | --- | --- |
| `AGENTS.md` | 总控入口 | 执行流程、路由、全局策略 | 极低 |
| `rules/` | 稳定规范 | 编码风格、测试规范、技术栈规则 | 低 |
| `skills/` | 可复用流程 | bugfix、refactor、feature-ui、feature-react | 中 |
| `memory/global/` | 跨项目沉淀 | 通用偏好、可复用模式、演化日志 | 中 |
| `memory/projects/` | 项目隔离上下文 | 决策、坑点、项目模式、约束 | 高 |

### 单母体、多项目复用

这套系统的基本思路是：

- 入口只有一套
- 规则只有一套主干
- 技能尽量复用
- 差异放到项目记忆里解决

这样能减少重复配置，也能让经验真正积累起来。

## 目录说明

### `AGENTS.md`

总控入口。定义：

- 项目识别
- 技术栈识别
- rule / skill 加载顺序
- UI 任务路由
- plan 触发条件
- memory 与演化策略

这份文件是系统核心，不建议频繁修改。

### `rules/`

存放稳定规范。当前包含：

- `coding-style.md`：通用编码风格
- `testing.md`：验证与测试要求
- `change-policy.md`：哪些文件适合高频更新，哪些不适合
- `evolution.md`：memory / skill / rule 升级条件
- `frontend-react.md`：React 项目规则
- `backend-node.md`：Node 后端规则
- `taro-miniapp.md`：Taro / 小程序规则
- `ui-consistency.md`：UI 一致性规则
- `tailwind-conventions.md`：Tailwind 写法约束

### `skills/`

存放可复用流程。当前包含：

- `bugfix/`：通用 bug 修复
- `refactor/`：通用重构
- `write-tests/`：测试编写
- `api-change/`：接口变更
- `feature-ui/`：从 0 到 1 生成功能级 / 页面级 UI
- `ui-refine/`：优化已有页面，统一风格与质量
- `feature-react/`：React 实现层 skill

### `memory/global/`

存放跨项目通用信息：

- `preferences.md`：稳定开发偏好
- `reusable-patterns.md`：可复用模式
- `evolution-log.md`：升级记录

### `memory/projects/`

存放项目隔离记忆：

- `_template.md`：项目记忆模板
- `_index.md`：项目索引
- `{project}.md`：具体项目的上下文、决策、坑点、模式

## 演化机制

经验升级路径：

```text
project memory -> skill -> rule
```

### 什么时候写 project memory

- 项目特定的决策
- 这个项目里踩过的坑
- 局部但有复用价值的模式
- 尚未稳定、但值得记录的经验

### 什么时候升级为 skill

满足下面条件再考虑：

- 在同一项目重复出现至少 2 次，或多个项目都出现
- 有明确触发条件
- 有明确步骤
- 已验证有效

### 什么时候升级为 rule

满足下面条件再考虑：

- 多项目可复用
- 已经稳定
- 不依赖强业务语义
- 作为规范比作为流程更合适

## 隔离机制

为了避免不同项目之间互相污染，这套系统默认：

- 每个项目单独写 `memory/projects/{project}.md`
- 禁止把 A 项目的业务细节写进 B 项目 memory
- 技术栈和项目识别先于 skill 选择
- 记忆分为 `Summary` 和 `Detailed Records`

简单理解：

- 共性的东西进 rule / skill / global memory
- 项目特有的东西进 project memory

## 维护建议

- 高频更新 `memory/`
- 中频更新 `skills/`
- 低频更新 `rules/`
- 极低频更新 `AGENTS.md`

如果某个问题刚出现一次，优先写 memory。
如果某个流程已经稳定复用，再考虑升级成 skill。
如果某条规则已经跨项目稳定成立，再考虑升级成 rule。

## 常见问题

### 我需要给每个项目单独建 AGENTS.md 吗？

不需要。默认就是用这一套母体复用到多个项目。

### 项目差异写在哪里？

写到 `memory/projects/{project}.md`。

### 我应该优先改 rule 还是 skill？

优先不要动 rule。一般先改 memory，再改 skill，最后才是 rule。

### README 和 AGENTS.md 的区别是什么？

- `README.md` 是给人看的系统说明
- `AGENTS.md` 是给 agent 执行的规则入口

不要把 `AGENTS.md` 的详细执行流程复制进 README。

### 这套系统是不是完全技术栈中立？

不是。它当前明显偏前端产品开发母体，尤其偏 UI、React、Tailwind、产品页面生成与优化。

这不是缺点，而是有意收敛后的定位。
