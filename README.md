# AI-Data

Python 数据分析与 AI 全链路学习项目。

**学习人**：朱俊 · **开始**：2026-10-12 · **目录**：`D:\Codex Project\AI-Data`

**GitHub 仓库**：https://github.com/ZJ-lucky-0915/ai-data-learning

这个项目不是"抄一遍教程就完事"的练习册，目标只有一个：**拿到一份陌生数据，知道第一刀该往哪儿切**。
所以每一关都要求产出能给别人看的东西——一张图、一份报告、一个能跑的工具。

---

## 一、3 步跑起来

```powershell
# 1. 激活环境（每次打开终端都先做这步）
.\.venv\Scripts\Activate.ps1

# 2. 下载数据集到 data\raw\
python scripts\download_data.py

# 3. 启动 Jupyter，浏览器会自动打开
jupyter lab
```

在 PyCharm 里用：`Settings → Project → Python Interpreter → Add Local Interpreter → Existing`，
选 `D:\Codex Project\AI-Data\.venv\Scripts\python.exe`，之后打开 `notebooks\00_环境自检.ipynb` 点运行即可。

---

## 二、目录结构

```
AI-Data/
├── .venv/                  # 虚拟环境（不提交，重装看 requirements/）
├── 数据工程计划.md          # 数据工程支线 + 项目四/五
├── README.md               # 你在这里
├── requirements/
│   ├── base.txt            # 阶段 1-2：numpy pandas matplotlib jupyter seaborn plotly polars
│   ├── ml.txt              # 阶段 3：scikit-learn xgboost lightgbm
│   ├── dl.txt              # 阶段 4：torch transformers datasets huggingface_hub
│   └── llm.txt             # 阶段 5：anthropic openai langchain llama-index
├── notebooks/              # 学习与实验的唯一入口，一个 notebook 一节课
├── scripts/                # 可复用的工具脚本（下数据、清洗、导出）
├── src/                    # 成型的代码（项目三的 PDF 总结 CLI 放这里）
├── data/
│   ├── raw/                # 原始数据，只读不改。要改就复制到 processed
│   └── processed/          # 清洗后的中间产物
├── models/                 # 微调后保存的模型
└── outputs/                # 图表、报告、导出文件
```

两条纪律，从第一天就养成：

1. **`data/raw` 只读**。原始数据永远是"案发现场"，别在上面改，要改就落到 `processed/`。
2. **一个 notebook 一节课**。命名 `编号_主题.ipynb`，跑完清空输出再存，别留一堆中间垃圾。

---

## 三、学习地图

**两条线，共 9 周（54 个学习日）。** 主线跑完再进支线，中间只插入 SQL（第 2 周）——因为 SQL 和 pandas 是同一件事的两种表达，连着学能互相印证。

### Part 1 · AI 主线（6 周）

| 阶段 | 主题 | 代表库 | 关键产出 | 预计 |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 环境与工作流 | venv · pip · jupyter | 环境自检通过 | 2 h |
| 1 | 数据基础四件套 | numpy pandas matplotlib jupyter | **项目一**：Titanic 探索性分析 | 12–15 h |
| 2 | 数据增强 | polars seaborn plotly | polars 重写 + 交互式图表 | 6–8 h |
| 2.5 | SQL 与 SQL 引擎 | sqlite3 · duckdb | 用 SQL 重写项目一 + 窗口函数 | 12 h |
| 3 | 传统 ML | scikit-learn xgboost lightgbm | Titanic 生存预测 + 模型对比 | 10–12 h |
| 4 | 深度学习 | pytorch transformers huggingface_hub | **项目二**：IMDB 情感分类微调 | 16–20 h |
| 5 | LLM 应用 | anthropic openai langchain llama-index | **项目三**：PDF 总结 + RAG 问答 | 14–16 h |
| 6 | 收尾与汇报 | — | 三份项目 README + 汇报材料 | 3 h |

### Part 2 · 数据工程支线（3 周 + 1 周选做，项目驱动）

这条线**不做小练习，直接做真实项目**——知识点边做边学，产出直接进作品集。

| 项目 | 技术栈 | 展示什么 | 周期 |
| :--- | :--- | :--- | :--- |
| **项目四** NYC 出租车数据数仓 | DuckDB · dbt · Parquet · Airflow | 7000 万行四层建模、按月增量、幂等回填、20+ 数据测试 | 第 7–9 周 |
| **项目五**（选做）端到端数据平台 | Docker Compose · Superset | 一条命令就能复现的完整系统 | 第 10 周 |

配套知识点（随项目推进讲解，详见 `数据工程计划.md`）：

| 阶段 | 主题 | 代表工具 |
| :--- | :--- | :--- |
| 7 | 数仓分层与维度建模 | DuckDB |
| 8 | ELT 与数据测试 | dbt |
| 9 | 列式存储、分区与增量 | Parquet · DuckDB |
| 10 | Docker 与编排调度 | Docker · Prefect · Airflow |
| 11 | AI × 数据工程交叉 | FAISS / pgvector |
| 12 | 大数据（选学） | PySpark |

总投入 120–140 小时。按每天 3 小时、每周休一天（≈18 h/周）算，**约 9 周**（做选做项目则 10 周）。
数据工程细节见 `数据工程计划.md`。
每阶段都有"通关标准"，达标了再往下走；卡住就别往下，地基漏了后面全是坑。

---

## 四、进度表

做完一格就在 `[ ]` 里打 `x`。

**Part 1 · AI 主线**

- [x] **阶段 0** 环境与工作流　_2026-10-12 完成_
- [ ] **阶段 1** 数据四件套（numpy / pandas / matplotlib / jupyter）
  - [x] numpy（第 1 课，练习已批改：14 倍性能差距、axis、广播）
  - [x] pandas 上：读数据、看数据、选数据（第 2 课，练习已批改：五问、loc/iloc、缺失值三策略、CoW 陷阱）
  - [ ] pandas 下：groupby / merge / pivot_table（第 3 课，进行中）
  - [ ] matplotlib + jupyter 工作流（第 4 课）
- [ ] **项目一** Titanic 探索性分析报告
- [ ] **阶段 2** 数据增强（polars / seaborn / plotly）
- [ ] **阶段 2.5** SQL 与 SQL 引擎（sqlite3 / duckdb）
- [ ] **阶段 3** 传统机器学习（sklearn / xgboost / lightgbm）
- [ ] **项目一+** Titanic 生存预测模型
- [ ] **阶段 4** 深度学习基础（pytorch）
- [ ] **项目二** IMDB 情感分类微调
- [ ] **阶段 5** LLM 应用（anthropic / RAG）
- [ ] **项目三** PDF 总结 CLI 工具
- [ ] **阶段 6** 收尾与汇报

**Part 2 · 数据工程支线**

- [ ] **项目四** NYC 出租车数据数仓（ODS → DWD → DWS → ADS）
- [ ] **阶段 7–9** 配套知识点：数仓建模 / dbt / 列式存储与增量
- [ ] **阶段 10** Docker 与编排调度（Prefect / Airflow）
- [ ] **阶段 11** AI × 数据工程交叉点
- [ ] **项目五**（选做）端到端可复现数据平台
- [ ] **阶段 12** PySpark 与大数据概念（选学）

**作品集与 GitHub**

- [ ] 配好 GitHub 认证，本地 `git init`
- [ ] `nyc-taxi-warehouse` 发布（项目四）
- [ ] `imdb-sentiment-classifier` 发布（项目二）
- [ ] `pdf-summarizer` 发布（项目三）
- [ ] 整理 README / 架构图 / License / CI 徽章
- [ ] 写简历上的三段项目描述

---

## 五、数据集准备

| 数据集 | 用途 | 获取方式 |
| :--- | :--- | :--- |
| Titanic | 项目一、阶段 3 | `python scripts\download_data.py` 自动下载 |
| TMDB 5000 Movies | 项目一进阶、阶段 2 | `python scripts\download_data.py tmdb` 自动下载 |
| IMDB 影评 5 万条 | 项目二 | 阶段 4 用 HuggingFace `datasets` 库直接下载 |

前两个都走公开镜像，**不需要注册 Kaggle 账号**。哪天镜像失效了，再走 Kaggle 官方来源：

1. 注册 [kaggle.com](https://www.kaggle.com) → 头像 → `Settings` → `API` → `Create New Token`
2. 把 `kaggle.json` 放到 `C:\Users\<用户名>\.kaggle\kaggle.json`
3. `pip install kaggle`，然后 `kaggle datasets download -d tmdb/tmdb-movie-metadata -p data\raw --unzip`

> 大数据集别放 Git 仓库，`data/raw/` 已经在 `.gitignore` 里了。

---

## 六、密钥管理（阶段 5 之前必须做）

`.env.example` 是模板，复制一份改名成 `.env` 再填真实密钥：

```powershell
Copy-Item .env.example .env
```

`.env` 已被 `.gitignore` 忽略，**永远不要提交**。代码里统一这么写：

```python
import os

from dotenv import load_dotenv

load_dotenv()  # 把 .env 里的键值读进环境变量
key = os.environ["ANTHROPIC_API_KEY"]
```

顺便一句：桌面上那个明文存 API 密钥的文件，等学到阶段 5 时一起收拾——
密钥一旦进了 Git 历史，想彻底清除非常麻烦。

---

## 七、怎么用这个项目学习

**从第 4 课开始改了练习方式**：讲一段、练一段，不再是所有练习都堆到最后。

每节课的结构变成：

1. **讲一个知识点** → 代码示例 → **立刻跟一个 2–5 分钟的小练习**
2. 小练习不给"答案"，但都写了 **"你应该观察到什么"** —— **看到了才算过**
3. 一个章节讲完，最后一节是 **3–4 道综合大练习**（要能交付、能拿给别人看）

**为什么这么改**：知识有保质期。全堆到最后做，前面讲的已经凉了；
而小练习的作用是**当场暴露误解**——错在刚讲完的地方，改起来最便宜。

你要做的：

1. 按顺序走，**别跳小练习**（它们才是让知识落地的地方）；
2. 卡住就把报错和你的思路贴给我；
3. 每节课结束写 3 行复盘：学了什么 / 卡在哪 / 下次怎么避。

遇到报错先别慌，也先别直接问。**先读报错的最后一行**——Python 的报错信息是写给人类看的，
90% 的问题最后一行就说了答案。

---

## 八、本机环境实况（2026-10-12 实测）

| 项目 | 实际情况 | 对学习的影响 |
| :--- | :--- | :--- |
| 系统 | Windows 11 | 路径用反斜杠，命令走 PowerShell |
| Python | 3.13.9（在 `D:\develop\Python`，全局） | 已建独立 venv，不污染全局环境 |
| CPU | Intel，16 线程 | 传统 ML 够用；深度学习只能小样本 |
| 显卡 | **无 NVIDIA 独显** | 阶段 4 本地 CPU 小样本跑通流程，正式训练上 Colab 免费 GPU |

已经装好的版本（2026-10-12 实测，pip 清华镜像）：
numpy 2.5.4 · pandas 3.0.6 · matplotlib 3.11.2 · seaborn 0.13.2 · plotly 7.1.0 · polars 2.0.0 · jupyterlab 4.6.4

**没有独显不是问题。** 阶段 4 的目标是"看懂微调流程"，不是"训出 SOTA"。
本地用 4000 条样本把整条链路跑通（约 40 分钟），想要漂亮准确率就上
[Google Colab](https://colab.research.google.com) 用免费 T4 跑全量 2.5 万条。
小机器调通、大机器训练，这本来就是工业界的常规做法。

---

## 九、安装与缓存目录规范

**一条规则：工具装 `D:\develop\` 下，缓存放 `D:\develop\cache\` 下。** 别再出现"这里一个那里一个"的情况——C 盘只剩 62 GB，一个模型下来就是几个 GB。

### 你的东西现在都在哪（2026-10-12 实测）

| 类型 | 位置 | 说明 |
| :--- | :--- | :--- |
| Python | `D:\develop\Python` | 全局解释器，3.13.9 |
| JDK 25 | `D:\develop\JDK` | IntelliJ 项目在用 |
| JDK 17 | `D:\develop\jdk17` | 已存在。PySpark 需要它（Spark 不支持 Java 25） |
| PyCharm / IDEA | `D:\develop\PyCharm 2026.2.1`、`D:\develop\IDEA` | |
| Git | `D:\Program Files\Git` | 保持不动 |
| ollama | `D:\develop\ollama` | 本地跑小模型，已有 `deepseek-r1:1.5b` |
| 本项目环境 | `D:\Codex Project\AI-Data\.venv` | 每个项目一个，互不干扰 |
| 项目数据 | `D:\Codex Project\AI-Data\data\` | 原始数据 + 中间产物 |

### 新增的统一位置

| 用途 | 位置 | 由哪个环境变量控制 |
| :--- | :--- | :--- |
| pip 下载缓存 | `D:\develop\cache\pip` | `PIP_CACHE_DIR` |
| HuggingFace 模型与数据集 | `D:\develop\cache\huggingface` | `HF_HOME` |
| PyTorch 预训练权重 | `D:\develop\cache\torch` | `TORCH_HOME` |
| ollama 模型 | `D:\ollama_models` | `OLLAMA_MODELS` |
| Docker 程序与镜像数据 | `D:\develop\Docker` | 安装时指定，镜像目录也要迁 |

这几个环境变量已经写成**用户级变量**，以后新开的窗口都会自动生效。
**已经在运行的 PyCharm 需要重启一次**才能读到。

> 一个必须知道的点：这些缓存目录不是"下载到那就完事"，而是**模型越攒越多**。
> 阶段 4 下 HuggingFace 模型、阶段 5 下数据集，动辄几个 GB。
> 如果哪天你发现 C 盘又满了，先来这张表里找原因。

---

## 十、常见坑

| 症状 | 原因 | 解决 |
| :--- | :--- | :--- |
| 图里中文变方框 `□□□` | matplotlib 默认字体不含中文 | `plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]` |
| 负号显示成方块 | 同上 | 加 `plt.rcParams["axes.unicode_minus"] = False` |
| `pip install` 慢 | 默认走国外源 | 加 `-i https://pypi.tuna.tsinghua.edu.cn/simple` |
| `ModuleNotFoundError` | 解释器选错，用了全局 Python | PyCharm 里确认是 `.venv\Scripts\python.exe` |
| plotly 图不显示 | 渲染器不对 | 结尾写 `fig.show()`，或 `fig.write_html("outputs/x.html")` |
| 下载数据集失败 | 网络或来源失效 | 重跑 `scripts\download_data.py`，或按第五节手动下 |
| 给某列赋值但值没变，又不报错 | **pandas 3.0 默认开启 Copy-on-Write**，链式赋值静默失效 | 别写 `df[df.a > 1]["b"] = 0`，改成 `df.loc[df.a > 1, "b"] = 0` |


