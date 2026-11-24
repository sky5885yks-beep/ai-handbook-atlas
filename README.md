# AI Handbook 导航地图

把散落在 GitHub 上的 AI / LLM / Agent handbook 仓库画成一张可走的地图：按生态层级分区，用推荐路线串起来。

- 在线地址：<https://37lf4zrsvx0csetmpgj.traesite.cn/>（当前仅自己可见）
- 形态：单文件静态站点（HTML + 内联 CSS/JS，无构建、无后端）
- 数据快照：2026-11-23
- 规模：34 个仓库、6 个生态层级、5 条推荐路线
- 参考风格：`sunxiaohui2025/AI-Infra-Handbook`
- 设计文档：[docs/DESIGN.md](docs/DESIGN.md)

## 功能

- 6 个生态层级：官方/机构、社区体系、工程推理 Infra、安全红队、具身语音、求职面试
- 34 个仓库节点，展示 star、最近推送、License、维护状态
- 节点状态：`active` / `slow` / `stale` / `caution`
- 5 条推荐路线：系统入门、上手 Agent、啃推理与 Infra、安全与红队、求职准备
- 实时搜索：仓库名、描述、层级
- 节点详情面板：定位、状态、License、推荐理由
- 键盘与 `prefers-reduced-motion` 支持
- 响应式：1080px 单列、680px 移动布局

## 目录

```
.
├─ index.html              # 站点全部源码（样式、数据、交互）
├─ docs/
│  └─ DESIGN.md            # 信息架构、数据模型、视觉与交互设计
├─ scripts/
│  └─ check_site.py        # 零依赖静态检查
├─ .github/workflows/ci.yml
├─ CHANGELOG.md
└─ README.md
```

## 本地预览

```bash
python -m http.server 8000
# 打开 http://localhost:8000
```

## 修改数据

所有内容都在 `index.html` 的脚本区：

- `BANDS`：6 个层级（`id/no/title/desc/official`）
- `REPOS`：仓库节点（`id/f/s/d/l/st/band/t/n`）
- `ROUTES`：推荐路线（`id/name/ids`）

新增仓库时：

1. 在 `REPOS` 增加一条，`id` 用 `owner/repo`；
2. 选对 `band`，补 `s`（star）、`d`（最近推送）、`l`（License）、`st`（状态）；
3. 如需进入路线，把 `id` 加进对应 `ROUTES.ids`；
4. 更新页脚快照日期；
5. 运行 `python scripts/check_site.py` 并本地预览。

## 数据口径

- star 与最近推送为 2026-11-23 的快照，会过期；
- 维护状态是按最近推送时间做的启发式判断，不是官方结论；
- 收录以“成体系的 AI/LLM/Agent 手册”为主，不追求全量；
- 站点为非官方整理，与所列仓库无隶属关系。

## 部署

当前部署在 TraeSite，源码以本仓库为准。更新 `index.html` 后重新部署即可；仓库保持私有，站点可见性由部署平台控制。

## 开发检查

```bash
python scripts/check_site.py
```

CI 会在 push / PR 时执行同一脚本。
