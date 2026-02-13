### Discussion format

Some of the lectures will be discussion-based. Each student will be assigned a paper and a role, and students with the same paper will be in the same group. You will prepare a summary according to that role before class, and during class you will create a short presentation for the entire class, which will then be used to seed a broader entire-class discussion. After class, you will post a reflection on the discussion you just had.

#### Discussion roles

To make the discussion more lively and engaging, we will adopt reading roles. Each student will play one of the following roles:

- *Citation Trail Archaeologist*: who places the paper in the broader research lineage by identifying key prior influence(s) and meaningful later response(s).
  - Identify **one key predecessor** (an older paper cited by the current paper) that substantially shaped the current paper’s problem framing, method, or evaluation.
    - In 2–4 bullet points: summarize the predecessor’s relevant idea/result and explicitly state what the current paper inherits/adapts.
  - Identify **one key successor** (a newer paper that cites the current paper) that meaningfully extends, replicates, operationalizes, or critiques it.
    - In 2–4 bullet points: summarize what the successor changes (e.g., metric, dataset, threat model, method) and whether it strengthens or weakens the current paper’s conclusions.
  - End with **one “lineage takeaway”**: one sentence on how the conversation changed from predecessor → current paper → successor.
- *Within-Week Connector*: who connects the assigned paper to the other papers being discussed this week and identifies tensions worth debating.
  - Choose **two** of the other assigned papers for the week.
  - For each chosen paper, write 3–5 bullet points addressing:
    - **Connection:** what shared question/setting/assumption makes these papers comparable?
    - **Key difference:** where do they diverge (definitions, threat model, measurement/metric, dataset/population, intervention point, conclusions)?
    - **Implication:** what would each paper say in response to the other?
  - Provide **one cross-paper discussion question** that forces the class to compare assumptions or evidence across papers.
- *Evaluation & Validity Auditor*: who audits whether the paper’s evaluation and evidence justify its headline claims. Focus on *validity threats* rather than generic “limitations.”
  - Identify one main claim of the paper and outline the “evaluation chain” (dataset/population → metric(s) → conclusion).
  - Discuss **at least two** concrete validity threats (e.g., construct/metric mismatch, baseline unfairness, confounds, distribution shift/external validity, subgroup validity).
  - For each validity threat, propose a feasible fix (an additional experiment, alternative metric, new slice, ablation, revised annotation protocol, etc.) and explain how it could change the conclusions.
- *Next-Step Study Designer*: who proposes one follow-up study that is only possible/meaningful because this paper exists, specified enough that someone could actually run it.
  - State a clear **motivation**, **research question** and (if applicable) **a hypothesis**.
  - Describe a **minimal study design**: dataset/population, metric(s), baseline(s)/comparisons, and what result would change your mind (a falsification criterion).
- *Methodology Challenger (Alternative Methods Advocate)*: who proposes a plausible alternative way to study the same question (method, measure, or study design) and argues how it could change the paper’s conclusions.
  - Identify **one key methodological choice** the paper relies on (e.g., study setting, participants, tasks, dataset/labels, metric, analysis).
  - Propose **one concrete alternative methodology** (e.g., field deployment instead of lab study; interviews instead of survey; different operationalization/metric; different comparison condition) and what you’d measure instead.
  - In 2–4 bullet points: explain **what validity risk** the alternative addresses and **how results might differ** (what outcome would strengthen vs weaken the paper’s claim).
  - End with **one discussion question** that forces the class to compare the paper’s method to your alternative using a specific result from the paper.

**Anchor requirements (apply to every role write-up):**

- In your writeup, include **at least two anchors** to the assigned paper:
  1) **One artifact anchor**: a specific figure/table/algorithm box/appendix result (e.g., “Table 2, row X…”), and  
  2) **One design-choice anchor**: a concrete methodological choice (dataset, labeling procedure, model family, threat model assumption, metric definition, prompt format, filtering policy, etc.).
- Role write-ups should be primarily bullet points and must include **one discussion question** that can’t be answered without referencing the paper’s specifics.

#### Per-role summary bullet point

In addition to your summary and proposed discussion question, each role must also submit a **1-sentence bullet point** that will be part of the summary slide for the paper.

- Within-Week Connector → Motivation
  - What is the state of the world and the possible problem that's being tackled?
- Citation Trail Archaeologist → Research Question
  - What is the main RQ they are asking?
- Methodology Challenger →  Approach & Method
  - How does the paper tackle the main research question? What is the key method?
- Evaluation & Validity Auditor → Key result/main finding
  - What is *one* main result from the investigation?
- Next-Step Study Designer → Takeaways
  - What is the main implication of the findings of this paper?

#### In-class discussion

- **20–30 minutes: small-group (“in-group”) discussion**
  - Each role should briefly share the key points from their notes (aim for ~2–3 minutes per role).
  - As a group, you will fill out a **one-slide summary for your paper** (intended to support discussion, not a formal presentation). *Your slides should include only what the rest of the class needs in order to engage with your discussion question.*
  - Please include the following in slide 1:
    - *Motivation*: What is the state of the world and the possible problem that's being tackled?
    - *Research Question*: What is the main RQ they are asking?
    - *Approach & Method*: How does the paper tackle the main research question? What is the key method?
    - *Key result/main finding*: What is one main result from the investigation?
    - *Takeaways*: What is the main implication of the findings of this paper?
  - Please include **one discussion** question that you settled on, on slide 2.
  
- **50–60 minutes: full-class discussion**
  - For each paper:
    - The group will give a **brief paper recap (max 1 minute)** using their slides, ending by stating their discussion question. I recommend having each group member stating their own bullet point.
    - We will then spend **~8–10 minutes** in full-class discussion. Discussion may include clarifying questions, critiques of assumptions/metrics, connections to other papers, and attempts to answer the group’s seed question.
  - **Participation grade:** every student must contribute to the full-class discussion **at least once** during the full-class meeting (e.g., ask a question, offer a critique, connect two papers, or respond to a peer’s point). One of the participation grades will be dropped.

- **Last 5 minutes: reflection**
  - Students will write a brief reflection identifying **one new thing** they learned from the discussion (conceptual insight, changed view, connection across papers, or a question they are still thinking about).

#### Discussion grading

- Pre-discussion summary (due day before class): 30%
- In-class presentation (graded as a group): 30%
- In-class participation (graded individually): 20%
- After class reflection (due midnight day of discussion class): 20%
