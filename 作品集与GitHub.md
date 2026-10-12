# 作品集与 GitHub 发布

> 目标：把学习成果变成**别人能点开看、能跑起来、能写进简历**的东西。
> 从第 1 周就开始用，别等到最后。

---

## 一、最终发布什么（精选 3–5 个，不贪多）

| 仓库名 | 来自 | 技术栈 | 展示什么 | 优先级 |
| :--- | :--- | :--- | :--- | :--- |
| `nyc-taxi-warehouse` | 项目四（数据工程） | DuckDB · dbt · Parquet · Airflow | 数仓建模、增量加载、调度、数据质量 | ★★★ |
| `imdb-sentiment-classifier` | 项目二 | PyTorch · transformers | 模型微调、评估、实验对比 | ★★★ |
| `pdf-summarizer` | 项目三 | anthropic SDK · RAG · 向量检索 | LLM 应用工程 | ★★ |
| `data-platform` | 项目五（选做） | Docker Compose · Superset | 一键复现的端到端系统 | ★★ |
| `ai-data-learning` | 学习记录 | Jupyter notebooks | 学习痕迹、SQL/pandas 练习 | ★ 可选 |

**宁可 3 个精致，不要 5 个半成品。** 招聘方在一个仓库上平均停留 30 秒，
他看的是 README 的前十行和目录结构，不是你的代码有多长。

---

## 二、一次性配置（做完就不用再管）

### 1. 身份 —— 已经配好了

```
user.name  = ZJ-lucky-0915
user.email = zjlucky0915@gmail.com
```

### 2. 认证方式，二选一

**方案 A：用已经装好的 Git Credential Manager（推荐，最省事）**

你机器上已经有 `credential.helper=manager`（Git for Windows 自带，我查过了），**什么都不用装**：

1. 第一次 `git push` 时会弹出凭据窗口
2. 选 `Sign in with your browser`，在浏览器里确认一次
3. 凭据会存进 Windows 凭据管理器，之后不用再管

**方案 A2：如果弹窗只给了账号密码输入框**，那就用个人访问令牌：

1. GitHub → 头像 → `Settings` → 左下角 `Developer settings` → `Personal access tokens` → `Fine-grained tokens` → `Generate new token`
2. 权限只勾 `Contents: Read and write` 就够
3. 生成后**立刻复制**（页面关掉就再也看不到）
4. 用户名填 `ZJ-lucky-0915`，**密码处粘贴 token**（不是账号密码）

**方案 B：SSH 密钥**

```powershell
ssh-keygen -t ed25519 -C "zjlucky0915@gmail.com"     # 一路回车
Get-Content ~\.ssh\id_ed25519.pub                     # 复制输出的公钥
```

粘贴到 GitHub → `Settings` → `SSH and GPG keys` → `New SSH key`。
之后远程地址用 `git@github.com:ZJ-lucky-0915/xxx.git`。

### 3. 代理

你的 git 配置里已经有 GitHub 代理（`http://127.0.0.1:7892`）。
push 的时候保持代理软件开着就行。

### 4. （可选）装 gh 命令行

```powershell
winget install GitHub.cli
gh auth login          # 引导式登录，比手动建 token 省事
```

装了之后建仓库就是一条命令：`gh repo create nyc-taxi-warehouse --public --source=. --push`

> **有一点我替你做不了**：创建 token 必须你本人在浏览器里登录 GitHub。
> 这一步你自己操作，卡住了叫我，我一步步带你。

---

## 三、README 模板（这决定 90% 的印象）

顺序很重要，招聘方是从上往下扫的：

1. **一句话说清这是什么** —— 别写"这是我的练习项目"
2. **架构图** —— ASCII 画的也行，用 draw.io 导出 PNG 更好
3. **数据来源与规模** —— 多少行、多大、什么时间跨度，**数字就是可信度**
4. **技术栈** —— 一行写完
5. **怎么跑起来** —— 三条命令以内
6. **结果与指标** —— 准确率、耗时、优化前后对比
7. **关键取舍** —— 2–3 条，这栏最能体现你是在思考还是在抄教程
8. **目录结构**
9. **License**（MIT 最适合作品集）

### 示例：`nyc-taxi-warehouse` 的 README 骨架

```markdown
# NYC Taxi Data Warehouse

基于 DuckDB + dbt 的四层数据仓库，处理 2023–2024 年纽约出租车行程数据（7000 万行），
支持按月增量加载与幂等回填。

## 架构

```
NYC TLC (Parquet, 公开 CDN)
        │  按月份增量抽取，水位线记录
        ▼
   ODS ── 分区 Parquet 落地（data/ods/year=2024/month=01/）
        │  清洗：异常金额/零距离/跨月行程、拆解时间字段、关联区域维度
        ▼
   DWD ── 明细宽表（dbt model）
        │  按小时 × 区域 × 支付方式聚合
        ▼
   DWS ── 汇总表
        │
        ▼
   ADS ── 面向分析的宽表（小费与支付方式的关系、高峰时段分布）
```

## 数据

| 项 | 值 |
| :--- | :--- |
| 来源 | NYC TLC Trip Record Data（官方公开，无需登录） |
| 规模 | 24 个月 · 约 7000 万行 · 原始 Parquet 约 1.1 GB |
| 维度表 | taxi_zone_lookup.csv（265 个区域） |

## 技术栈

`DuckDB` · `dbt-core` · `Parquet` · `Prefect` / `Airflow` · `Python 3.13`

## 快速开始

```bash
git clone https://github.com/ZJ-lucky-0915/nyc-taxi-warehouse.git
cd nyc-taxi-warehouse
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
python scripts/extract.py --start 2023-01 --end 2024-12   # 首次约 10 分钟
dbt build
```

## 结果

- 全量构建耗时 **2 分 18 秒**（7000 万行 → 4 层 11 张表）
- 增量更新单月耗时 **7 秒**
- dbt 数据测试 **23 个**，全部通过
- DWS 汇总后，常用分析查询从 14.2 秒降到 **0.4 秒**

## 关键取舍

- **用 DuckDB 而不是 Spark**：数据量 7000 万行、单机 16 核能扛，
  引入 Spark 只会增加运维复杂度而不会更快。什么时候该上 Spark 我在文档里写了自己的判断标准。
- **全量重算 vs 增量**：DWD 层选增量（省时间），DWS 层选全量重算
  （数据量小、逻辑常改、避免增量的状态管理成本）。
- **清洗放在 DWD 而不是 ODS**：ODS 保持贴源，任何清洗规则的变化都不需要重新下载数据。

## License

MIT
```

---

## 四、简历上怎么写

公式：**动词 + 技术栈 + 规模数字 + 结果**。

```
- 设计并实现基于 dbt + DuckDB 的四层数据仓库，处理 7000 万行纽约出租车行程数据；
  实现按月增量加载与幂等回填，23 个 dbt 数据测试覆盖唯一性/非空/枚举/引用完整性。
- 通过列式存储与分区裁剪优化查询，常用分析查询耗时从 14.2 秒降至 0.4 秒。
- 用 Prefect 编排日更管道，支持失败自动重试与历史回填；配合 dbt 血缘图定位数据问题。
```

**反例**（很多人这么写，等于没写）：

```
- 熟悉 pandas、numpy、sklearn 等常用库
- 学习了 dbt 和 Airflow
- 参与数据分析项目
```

区别在哪：前者有**规模**（7000 万行）、有**具体动作**（增量加载、幂等回填）、
有**可验证的结果**（14.2 秒 → 0.4 秒）。后者只说明你见过这些词。

---

## 五、别踩的坑

### 绝对不能提交的东西

| 文件 | 原因 |
| :--- | :--- |
| `.env` | API 密钥。**一旦提交，Git 历史里很难彻底清除**，必须作废重发密钥 |
| `kaggle.json` | 同上 |
| 原始数据 | 几十上百 MB，别人 clone 会痛不欲生。README 写清楚下载命令就行 |
| 模型权重 | 同上。或者用 Git LFS |
| `.venv/`、`__pycache__/`、`.ipynb_checkpoints/` | 垃圾文件 |

**自检命令**（push 之前跑一遍）：

```powershell
git status                              # 看有没有意外文件
git diff --cached --name-only           # 看暂存了什么
git log -p -S "sk-ant" --oneline        # 搜历史里有没有漏过 API key
```

> 顺便提醒：你桌面上那个明文存 API 密钥的文本文件，早晚要收拾。
> 学到阶段 5 的时候我们一起处理掉。

### commit 历史

- **从第 1 周就建仓库，边做边提交。** 真实的历史本来就比最后一次性 push 好看。
- 提交信息用前缀：`feat:` 新功能 · `fix:` 修 bug · `docs:` 文档 · `refactor:` 重构
- 别出现 `update`、`修改`、`111` 这种提交信息
- 一个小技巧：把每天的进展拆成 2–3 个小提交，而不是一个大提交——既清晰又诚实

### 加分项

- **GitHub Actions**：每次 push 自动跑 `dbt test` 或 `pytest`，
  README 顶部挂一个绿色的 passing 徽章。这一个小动作就能让你和 90% 的候选人区分开。
- 加 `LICENSE` 文件（MIT）
- 仓库顶部加 Topics 标签：`data-engineering` `dbt` `duckdb` `pyspark`
- 固定（Pin）到 GitHub 个人主页，招聘方点进来第一眼就能看到

---

## 六、按周的执行安排

| 时间 | 做什么 |
| :--- | :--- |
| 第 1 周 | 配好认证方式；本地 `git init`，把 AI-Data 变成仓库并提交第一次 |
| 第 1–6 周 | 每个项目做到"能用"时就建仓库、push，不要攒到最后 |
| 第 7–9 周 | 项目四边做边提交，README 同步写（不是最后补） |
| 第 9 周末 | 整理 3 个主力仓库：架构图、License、CI 徽章、Topics |
| 第 10 周 | 写简历上的三段项目描述；可选做项目五 |

---

## 七、第一次发布的操作步骤（我会带你做）

```powershell
# 1. 在项目目录里初始化
cd "D:\Codex Project\AI-Data"
git init
git add .
git commit -m "chore: 初始化 AI-Data 学习项目"

# 2. 在 GitHub 网页上新建一个空仓库（不要勾选 README / .gitignore）
#    仓库名：ai-data-learning

# 3. 关联并推送
git remote add origin https://github.com/ZJ-lucky-0915/ai-data-learning.git
git branch -M main
git push -u origin main
```

第一次 push 会弹窗要凭据，用户名填 `ZJ-lucky-0915`，密码粘贴 token。

---

## 八、仓库怎么放（一个结构问题，先定下来）

```
D:\Codex Project\
├── AI-Data\                       # 仓库 1：ai-data-learning —— 学习记录 + 项目一
│   ├── notebooks\                 #   课程练习
│   ├── scripts\  data\  src\
│   └── 学习计划.md  数据工程计划.md  作品集与GitHub.md
├── imdb-sentiment-classifier\     # 仓库 2：项目二（独立仓库）
├── pdf-summarizer\                # 仓库 3：项目三（独立仓库）
└── nyc-taxi-warehouse\            # 仓库 4：项目四（独立仓库，主力）
```

**为什么不把所有项目塞进一个大仓库**：

- 简历上要给每个项目单独一个链接；
- 招聘方点开一个仓库，看到的是**一个完整的东西**，而不是"在一堆练习里翻找"；
- 仓库体积可控，三个项目的依赖和数据不用混在一起。

代价是每个项目要单独配置（`git init`、依赖、README）。
但这本来就是真实工作的样子——一个仓库一个职责。

所以从项目二开始，我会在 `D:\Codex Project\` 下新建独立目录，
而不是继续往 AI-Data 里堆。AI-Data 只负责"学习记录 + 项目一"。
