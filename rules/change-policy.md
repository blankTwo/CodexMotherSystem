# Change Policy

## Allowed High Frequency Updates
- memory/global/*
- memory/projects/*

## Allowed With Reason
- rules/*
- skills/*

## Forbidden Automatic Updates
- AGENTS.md

### AGENTS.md Exception
当用户明确要求以下任务时，允许修改 AGENTS.md：
- Agent OS 架构调整
- Gate 定义或执行流程调整
- 总控规则修订
- Project / Stack / Task Layer routing 调整

修改 AGENTS.md 前必须说明：
- 修改原因
- 影响范围
- 验证方式

修改 AGENTS.md 后必须：
- 触发 Review Gate，或执行等价一致性检查
- 检查 README / rules / skills 是否出现职责重复或旧规则残留
- 说明是否需要 memory / evolution 记录

## Promotion Standard
只有当某经验满足以下条件，才允许升级：
- 已验证
- 可复用
- 有明确边界
- 非一次性技巧
- 非强业务耦合

## Skill / Rule Maintenance
- 修改 skill 前必须说明复用价值和触发场景
- 修改 rule 前必须说明为什么它已经足够稳定
- 不把单个案例、临时 workaround 或未验证偏好写进 skill / rule
- 优先增强已有 task-layer skill，不因为出现新技术栈就新增 stack-specific skill
- 修改后应检查描述是否仍准确，避免 skill 触发范围过宽
- 新增 stack-specific skill 必须有跨项目证据、清晰边界，并证明不能由 task-layer skill + project pattern 解决

## Review Gate
修改以下内容时，应执行 `rules/review-gate.md`：
- AGENTS.md
- rules/*
- skills/*
- 大范围架构或跨任务层变更
- 权限、数据、安全、支付、发布等高风险修改

## Anti-Drift
- 不得为了“更通用”而破坏已有清晰流程
- 不得为了“更智能”而让规则不可执行
- 规则必须简洁、明确、可操作
- 新规则必须能回答“何时触发、如何执行、如何验证”
