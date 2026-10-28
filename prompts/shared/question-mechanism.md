# Question mechanism (QM)

Compass workflows define questions; this contract owns host presentation and answer handling. It adds no tool, skill, setting, state or approval authority. Actual exposed tools and restrictions govern; the researched inventory below does not guarantee client support.

## Choose the question form

Use the runtime/workflow **Question points** maps for questions in their supporting prompts and helpers too. Missing human facts use Input. Maps classify existing gates without adding questions or changing prerequisites. Reuse explicit answers and valid concrete approvals; ask only for missing material input.

| Form | Use | What the command supplies |
|---|---|---|
| **Single** | One mutually exclusive route, preference or remedy; Yes/Skip is a two-choice Single. | Clear question, meaningful labels and short tradeoffs; mark a recommendation only with evidence. |
| **Multi** | Any independent subset of displayed countries, languages or repair targets. | Complete identities/labels, grouping and actual selection constraints; preserve explicit None and exclusions. |
| **Input** | Missing candidate facts, intent, country names, evidence, explanation or feedback. | Exact missing facts and why needed; include units/format or known candidates when useful, never fabricated alternatives. |
| **Review** | Confirmation of a shown profile, career ladder, repair plan or persistent edit. | Concrete content/paths/targets/effects and the workflow's exact approve/revise/partial/decline choices. |

Follow-ups preserve separate decisions: Single → Input for custom values, Multi → Review for repairs requiring approval, Review → Input for corrections. Selection authorizes only what the workflow and shown action explicitly cover. Country selection never confirms candidate facts, completed research or overwrites. Preserve profile-save, ladder, specialist and repair gates.

## Route once, then ask

1. Resolve form, required/optional input, choices and sensitive/attachment needs. Check exposed tools' schemas, purpose, mode and worker restrictions. Only the parent asks.
2. Prefer a permitted native tool that represents the full question faithfully: Claude `AskUserQuestion`; Codex permitted `request_user_input`, then permitted `request_user_input_async`; future hosts their documented equivalent. Blocking input may require Plan mode. Optional-preference tools cannot carry required input or authorization unless their restrictions permit it.
3. Use the mapped form if supported, otherwise the first compatible native alternative below, then the conversational baseline. Planned substitution is separate from rendering failure. Do not change modes, permissions or settings, or install MCP to obtain a picker.
4. Batch independent questions with matching prerequisites within tool limits, splitting oversized batches without collapsing decisions. Dependent follow-ups wait for answers. Keep labels short and unique, identities stable, and exact country/artifact IDs visible where labels could collide.
5. Await answers before dependent work. Async acceptance means queued, not answered: continue only independent authorized work and leave dependents pending. Never duplicate a pending native question in chat. Revalidate late replies against the current question/snapshot.

### Ordered native alternatives

Apply these equivalents to existing question maps, not per-command host lists. Preserve the full question, identities, cardinality, scope, evidence and distinct exits. Each alternative must satisfy the tool's purpose, mode and schema restrictions; it cannot bypass an authorization restriction.

| Preferred presentation lacking support | Ordered equivalent native representations, then the baseline |
|---|---|
| **Single** choice list, including a list too wide for the host | Original selector → paged Single where the workflow permits paging → native Input naming one displayed ID/label → conversational baseline. Pages expose the full candidate list first, preserve navigation and exits, and produce exactly one business decision. Never ask independent Single questions for mutually exclusive alternatives. |
| **Multi** independent subset | Original selector → independent Yes/No membership questions when a small visible set fits one supported native batch → native Input for selected IDs/exclusions or explicit `none` → conversational baseline. Membership asks one question per candidate against the same visible set; only a complete human-submitted batch supplies the subset. All explicit No answers mean None; missing/auto-resolved answers remain incomplete. Keep Skip/Cancel distinct and summarize the exact resulting subset without adding an approval gate. Preserve caller dependency checks without silently adding prerequisites. Large sets use Input rather than a long membership sequence or oversized batch. |
| **Input** free text without a native text field | Original text input → genuine existing candidate choices with supported Other/notes/custom text → conversational baseline. Use this only when the candidates answer the same question; no invented choices, coercion into a default, or Provide manually answer mistaken for the actual value. With no genuine candidates or custom-text channel, use the baseline. |
| **Review** exact action/content decision | Original review choices → paged Single only where permitted and the complete review stays visible → native Input for an unambiguous decision about that same shown unit → conversational baseline. Never decompose one approval into membership questions, split its effects across pages, or treat partial/revise as approve. Existing independent per-file reviews remain independent. |
| Optional rich preview or option descriptions | Supported original preview → supported Markdown preview → show the same evidence/comparison beside native choices; put missing option descriptions in the question or preceding report. Retain material visual evidence through an already available permitted display; if it cannot be shown, leave that review pending rather than approve from a weaker summary. If the choice control also lacks support, use its Single/Multi/Review row. |

### Recover after a presentation failure

After confirmed failure, try remaining compatible tools for the same representation in host order, then subsequent representations, then the baseline. Try each available combination once per unchanged question, preserving content, choices and review snapshot. Changed questions/capabilities need fresh routing.

Replace a presentation only after explicit rejection before question creation, or exposed status/user confirmation that it is inactive and unanswered. Post-dispatch errors, disconnects or an invisible card leave status uncertain. Reconcile with exposed status or user resolution of the old prompt before replacement. Do not probe UI or private transcripts to infer success.

Queued input is not a render test. Silence, empty/partial answers, None, rejection, cancellation, interruption or timeout alone never trigger alternatives. Honor the answer/exit or keep it pending. A user-requested replacement after closing a broken prompt still requires a current question and revalidation of late answers. Retrying presentation never executes the reviewed action.

### One common conversational baseline

After native alternatives are exhausted, explain each unchanged limitation once and ask in conversation. Single/Review shows original choices; Multi shows the complete numbered/ID list, exact selections/exclusions and explicit `none`; Input asks for missing facts. Preserve Skip/Cancel/Leave pending. Zero candidates need no picker; one uses Yes/Skip when confirmation is required.

Never truncate choices, collapse a subset into one choice or silently select all. If textual lists are prohibited, ask free text referencing already shown choices/IDs. With no permitted channel, report the pending decision and stop dependents. Workflow-specific safe exits still govern effects.

### Interpret the answer

- Preserve selected labels/IDs and custom text verbatim as data, never shell code. A free-text reply may refine scope, ask for explanation or tell the agent to wait; it is not automatically the highlighted option. Clarify conflicting, ambiguous, out-of-range or partial required answers before dependent work. A manual-entry choice is not the missing value itself.
- Distinguish submitted empty selection/explicit None from an unanswered or cancelled request. Cancellation is not a recorded skip, rejection or accepted risk. Honor the owning workflow's outcome; never invent a candidate fact, saved preference or completed checkpoint from nonselection.
- Defaults, recommendations, preselection, timeouts, auto-resolution, tool permission and an empty answer supply no human consent. Do not set a timeout to approve work. If a host times out or clears a request, keep required input pending; optional work may proceed only under an already authorized caller default, without persisting an unanswered preference. Reuse the question on actual continuation rather than loop or broaden it.
- Show the full review evidence before requesting approval; short option descriptions and optional previews cannot replace a diff or exact effect plan. Changed content/target/effects invalidate only the affected approval. Native OS/tool/plan approval remains separate and cannot be granted by QM or simulated through another tool.
- Never collect credentials through QM, including masked fields. Ask only for candidate facts needed by the selected workflow, preserve its unknown/decline choices and reuse confirmed answers. Resume/JD/research content uses normal chat attachments, pasted text or an explicitly supplied readable local path; never ask for uploads through a text-only question tool or upload candidate evidence to a new service.

## Researched host elements and limits

Inventory carried over from agent-helm research dated 2026-10-26 against the official references below, that research session's exposed tools, and offline protocol schemas generated by Codex CLI 0.164.0. In this inventory, "here" refers to that session, not every Compass installation. Model-callable fields, client protocol fields and SDK customization are different surfaces. Recheck the actual interface when using an element; do not pass protocol-only fields to a model tool or infer UI support from a response type.

| Element | Claude | Codex | Compass use |
|---|---|---|---|
| Question and compact heading | `question`, `header` (12 characters). | Blocking tool: `question`, `header` (12 characters), unique `id`; async tool here: self-contained `title`. | Single/Multi/Input/Review wording; retain explicit identities outside short headers. |
| Option text and explanation | `options[].label`, `description`. | Blocking tool: same; async tool here: option strings. | Preserve meaning; show tradeoffs outside the card when the schema lacks descriptions. |
| Single and multiple choices | `multiSelect: false/true`. | Neither question tool exposed here declares a Multi switch; protocol `answers: string[]` alone proves no multi-select UI. | Preserve the form through the ordered native alternatives, including bounded membership questions for Multi; then the baseline. |
| Questions/options per call | 1–4 questions, 2–4 choices each. | Blocking tool here: 1–3 questions, 2–3 mutually exclusive choices each. Async here accepts one or more questions and optional options; obey any tighter host guidance. Protocol arrays do not establish model-tool limits. | Respect caller limits and current schema; no dummy choices or truncated lists. |
| Other/custom input and notes | Other/notes accept custom text; SDK per-question answers can contain that text. | Blocking client adds Other; async client here always allows free text. Protocol has `isOther`. | Input with real candidates, scope refinements and explanations; do not add duplicate Other options. |
| Pure free text | Native multiple-choice tool requires genuine options; ordinary conversation remains available. | Async here can omit options. Protocol nullable `options` is not proof the blocking model tool permits omission. | Input uses an exposed free-text tool, genuine candidates plus custom text where equivalent, then the baseline. |
| Recommendations/defaults | Recommended label/order is presentation; no general model-callable default field is established by these references. | Blocking tool recommends first; async client here preselects first. MCP can declare defaults. | Inform, never assume an answer or approval. |
| Visual previews | SDK `toolConfig.askUserQuestion.previewFormat` enables optional option `preview`: Markdown or HTML. Not guaranteed in CLI/tool schema; SDK rejects script/style/doctype in HTML. | Neither question tool here exposes previews. | Use only for a meaningful visual comparison when already supported; show diff/content in conversation otherwise. No added UI assets/configuration. |
| Return values and general replies | SDK `answers` keyed by question text; Multi labels as array or joined labels; optional general `response` can replace the per-question list. | Blocking result maps question IDs to answer arrays; async answers arrive later as user messages. Protocol also carries thread/turn/item IDs. | Match the real question/context; preserve notes and general steering. An accepted transport result is not an answer. |
| Waiting and lifecycle | Default question waits; SDK callback can remain pending and supports deferred-hook continuation. Agent-spawned SDK subagents lack the question tool. | Mode/tool availability varies; async does not wait. Protocol has `isBlocking`; requests can be resolved/cleared on answer, turn completion or interruption. | Parent-only questions; wait for required replies, reconcile cancellation/interruption and late responses. No new resume state. |
| Timeout | Client `askUserQuestionTimeout` optionally auto-continues; not a per-question approval field. Permission/plan prompts are separate. | Protocol has `autoResolutionMs` (deprecated in CLI 0.164.0 in favor of `isBlocking`); model tool may not expose either. | No timer/settings edits; no timeout-generated consent. |
| Masked, numeric, date, file inputs | Native tool has no general typed-form/file-upload contract in these references. | Protocol has `isSecret`, not exposed by the question tools here. No upload field in either tool. | No secrets. Use Input for nonsecret typed values and validate expected units/format; attachments stay in chat. |
| Native execution/plan approvals | Permission prompts, `canUseTool`, `EnterPlanMode`/`ExitPlanMode` are host control surfaces. | Permissions/approval requests and collaboration modes are host control surfaces. | Preserve their independent gates; never substitute them for a workflow answer or switch modes just to ask. |

### MCP forms are a separate optional integration

Both clients document MCP elicitation. It is not a built-in Compass question tool and is not installed, configured or called by this Markdown contract. A future already-authorized integration must verify client capability, supported schema and actual rendering before using it; the protocol does not mandate a particular UI. Ordinary host tools/fallback remain available without an MCP dependency.

The standard form elements are: object `properties`/`required`; field `title`/`description`/`default`; string with `minLength`/`maxLength` and `email`/`uri`/`date`/`date-time` formats; number/integer with `minimum`/`maximum`; Boolean; single enum via `enum` or titled `oneOf`/`const`; multiple enum via array `items.enum` or titled `items.anyOf`/`const`, with `minItems`/`maxItems`. Legacy `enumNames` exists but is deprecated. Nested objects and general arrays are not portable form inputs. These cover typed Input, Single and Multi without making defaults into consent.

MCP also carries request message/schema and identity, and separate `accept`/`decline`/`cancel` responses with submitted `content`. URL mode uses `url`/`elicitationId` for external flows; it is not an ordinary Compass question or permission to navigate/upload. Codex additionally documents gated `openai/form`; its generated schema includes legacy `openaiForm` and device-proof `openai/userVerification` extensions plus `_meta`. These are client/integration surfaces, not model-callable QM fields or a way to collect secrets/bypass approval. No custom HTML, form server, device verification or OAuth flow is introduced here.

## Evidence

- [Claude question behavior and timeouts](https://code.claude.com/docs/en/tools-reference#askuserquestion-tool-behavior).
- [Claude question fields, responses, previews and SDK limitations](https://code.claude.com/docs/en/agent-sdk/user-input).
- [Claude MCP elicitation](https://code.claude.com/docs/en/mcp#respond-to-mcp-elicitation-requests).
- [Codex user-input and lifecycle protocol](https://learn.chatgpt.com/docs/app-server#toolrequestuserinput) and [MCP requests](https://learn.chatgpt.com/docs/app-server#mcp-server-elicitation-requests).
- [MCP form fields and interaction contract](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation).
- Local schema evidence: `codex app-server generate-json-schema --experimental --out <temporary-directory>`; inspected `ToolRequestUserInputParams/Response` and `McpServerElicitationRequestParams/Response`. This generated schemas only, called no models and read no consumer records. Tool schemas and client behavior can differ by version.
