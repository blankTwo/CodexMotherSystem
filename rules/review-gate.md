# Review Gate

Review Gate 用于核心规则、跨层改动和高风险修改完成后的结构化复核。

它不是所有小改动的必经流程；只有当 Risk Gate 或 change policy 触发时才执行。

---

## When To Run
以下情况建议或必须执行 Review Gate：
- 修改 AGENTS.md / rules / skills
- 跨任务层的全栈改动
- 权限、数据、安全、支付、发布相关改动
- 大规模重构或架构调整
- 发布前关键变更
- 多 Agent 并行后需要合并结果

---

## Review Checklist

### 1. Goal Fit
- 是否解决了用户明确要求的问题
- 是否引入了用户未要求的额外功能、抽象或流程
- 修改范围是否完整，但没有无故扩大影响面

### 2. Boundary
- 是否破坏了已有 rules / skills / gates 的职责边界
- 是否让某个 skill 承担过宽职责
- 是否把技术栈上下文误当成 skill 选择依据
- 是否新增了不必要的 stack-specific skill

### 3. Consistency
- 术语是否统一
- 是否存在旧定位、旧流程或旧规则残留
- README / AGENTS / rules / skills 是否出现双写冲突
- Rules Loading Order 是否仍然合理

### 4. Evidence And Validation
- 判断是否基于文件、代码、日志、测试或用户上下文
- 是否说明验证方式和验证结果
- 验证是否覆盖核心路径
- 是否标记无法验证项、部分通过项和剩余风险
- 性能相关任务是否有基线、目标或替代验证

### 5. Evolution And Memory
- 是否需要写 project memory
- 是否只是 `[candidate-skill]` 或 `[candidate-rule]`
- 是否满足 Trigger / Count / Validation / Scope / Boundary
- 是否避免把一次性操作、未验证偏好或普通成功路径沉淀

### 6. Executability
- 新规则是否能回答“何时触发、如何执行、如何验证”
- 是否足够简洁，避免过度抽象
- 是否存在执行者需要猜测才能遵守的描述
- 是否会导致无限循环、无限新增 skill 或无限扩展 memory

### 7. Risk And Rollback
- 是否识别了影响范围
- 是否需要回滚预案
- 是否需要 worktree 隔离
- 如果 review 不通过，是否知道应调整、回滚还是暂停确认

---

## Review Result

### Pass
适用条件：
- 核心目标已满足
- 无明显边界冲突
- 验证证据足够
- 剩余风险已说明

输出应包含：
- Review 结论：通过
- 检查范围
- 验证证据
- 剩余风险

### Pass With Notes
适用条件：
- 核心目标已满足
- 存在非阻塞风险、后续观察项或待验证项

输出应包含：
- Review 结论：有保留通过
- 保留项
- 为什么不阻塞本次交付
- 后续建议

### Fail
适用条件：
- 核心目标未满足
- 核心路径验证失败
- 规则边界冲突
- 修改引入明显不可执行规则
- 高风险修改缺少验证或回滚方案

处理方式：
- 记录不通过原因
- 停止扩大修改
- 优先修复不符合项并重新 review
- 必要时回滚到稳定状态或向用户确认方向

---

## What Not To Do
- 不要把 Review Gate 用在所有小改动上
- 不要只检查格式，不检查语义和边界
- 不要在 review 失败后仍然声称完成
- 不要在 review 时引入新的未经讨论的标准
- 不要用 Review Gate 替代 Evidence Gate 或 Validation Gate
