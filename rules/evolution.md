# Evolution Rules

## memory -> skill
满足全部条件时，允许从 memory 升级为 skill：
- Trigger: 触发场景清晰，能回答“什么时候用”
- Count: 在同一项目重复出现 >= 2 次，或跨项目出现 >= 2 次
- Validation: 有可复现验证证据，不能只靠主观判断
- Scope: 适用范围和不适用范围明确
- Boundary: 不会吞并其他 skill / rule 职责
- Reusable: 可被重复执行，不依赖特定业务上下文

## skill -> rule
满足全部条件时，允许从 skill 升级为 rule：
- 已作为 skill 稳定运行
- 跨项目可复用，通常需要 >= 3 个项目或等价证据
- 不依赖强业务语义
- 作为规范比作为流程更合适
- 不存在明显争议

## Candidate Marker
证据不足但可能值得升级的经验，只能先留在 project memory：
- `[candidate-skill]`: 等待第二次出现或跨项目验证
- `[candidate-rule]`: 等待 skill 稳定运行与跨项目证据

Candidate 必须记录：
- Trigger: 触发场景
- Count: 出现次数
- Validation: 已有验证证据
- Scope: 适用范围
- Boundary: 与现有 rules / skills 的边界

Candidate 不等于承诺升级。第二次出现时必须重新评估，而不是自动提升。

## Do Not Promote
以下内容不得升级：
- 一次性 workaround
- 强业务耦合技巧
- 仍存在明显争议的做法
- 缺少验证的经验
- 普通成功路径，没有形成可复用模式
- 只适用于单一技术栈但没有跨项目证据的实现细节
- 为了“显得完整”而补充的抽象规则

## Do Not Record
以下内容通常不需要写入 memory：
- 没有复用价值的临时操作
- 已由现有 rules / skills 覆盖的普通流程
- 没有新决策、新坑点、新约束的信息
- 用户明确表示只是一次性尝试或临时验证
- 未验证猜测、临时偏好或主观审美
- 只对当前文件命名或当前目录结构有意义的细节

## Promotion Output
升级时必须说明：
- 来源
- 为什么值得升级
- 适用范围
- 风险
- 触发条件
- 出现次数
- 验证方式

## Evidence Preference
演化记录优先使用结构化字段，而不是只写主观判断：
- Trigger: 在什么任务或场景下触发
- Count: 已出现次数，尽量写明确数字
- Validation: 通过什么验证证明有效
- Scope: 适用于哪些项目/模块/边界
- Boundary: 与哪些 rules / skills 相邻，如何区分
- Candidate: 建议停留在 memory、升级为 skill，还是升级为 rule

## Alignment With Change Policy
- memory -> skill 必须满足本文件的 memory -> skill 阈值
- skill -> rule 必须满足本文件的 skill -> rule 阈值
- 修改已有 rule 时，必须说明修改后为什么仍然稳定、可执行且不会破坏现有项目
- 不得为了“显得完整”把候选经验提前写入 rules / skills
