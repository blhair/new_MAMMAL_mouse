name: project_explorer
description: 分析并解释项目结构、数据结构和代码逻辑。支持生成project_map、解释数据文件格式、分析依赖关系。
mode: subagent
tools:
  - glob
  - read
  - grep
  - bash
  - task
