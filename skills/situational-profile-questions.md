---
name: Situational Profile Questions
description: Reuse confirmed candidate facts and collect material missing situational context for the active workflow.
---

# Situational Profile Questions

If situational-profile.md exists in the selected run, reuse it without restarting intake. Otherwise read the confirmed profile.md and this person's explicit answers in the selected run. Reuse applicable location, citizenship, languages, status and preferences; ask only for material missing or conflicting facts. Do not infer current facts from stale history, work rights from residence/citizenship, or acceptable working languages from spoken ability.

Use these short questions only for unresolved context needed by the caller. Batch independent missing facts within QM limits. Keep the answer-handling instructions below agent-facing; add only a brief hint when needed for a usable answer.

For Country Finder and Salary Calculator, location, citizenship, working languages and relevant work rights/status are core context. Ask once for missing core answers before proceeding; an omission is not an explicit unknown or declined answer. Accept an actual unknown/decline without repeating the question or inventing the fact.

1. Where are you currently based?
2. What is your citizenship or passport nationality?
3. Which languages are you willing and able to work in?
4. What work rights or immigration status do you hold, and where? (country + status)
5. Do you have a minimum monthly pay requirement? (optional)

## Answer handling

Request a city/timezone only when needed for a comparison. Citizenship supplies the nationality context for immigration research; reuse confirmed citizenship as that status fact where relevant, without asking twice. For country-specific status, retain citizenship, permanent residence, visas and any known work conditions; accept "none" / "unknown". A status label does not alone establish unrestricted permission. Keep nationality and status distinct and do not re-ask established residence.

Use the language answer for accepted main working languages and self-reported ability, not a separate spoken-language inventory or invented proficiency level. Preserve resume languages; clarify proficiency only when material.

The pay question is optional for both commands. "Not specified" means no personal floor, not zero; Salary Calculator must not require users to know their expected salary before researching it. For a supplied minimum, collect only unresolved amount, currency and gross base versus net/take-home basis: "What amount and currency, and is it gross base or take-home pay?" Clarify hard floor versus context only when ambiguous: "Is that a firm minimum or just context?" Never ask permission to choose a local-market midpoint; its evidence-backed selection belongs to the salary research.

Country Finder uses a hard floor only under its track-specific comparison rules. Salary Calculator uses it only for the Step 4/5b Summary flag, never to filter countries or change either target. Context-only answers remain context in both commands. Apply skills/salary-comparison-rules.md before any comparison.

## Conditional context

Neither command asks users to assess general citizenship-related immigration friction or employer risk perception. Research applicable restrictions and employer evidence. Ask about a personal circumstance only when a concrete research gap makes it relevant; a user-confirmed personal case fact differs from a general perception that needs verification. Preserve supplied concerns and legacy answers as research leads, not verified restrictions or automatic salary penalties. Keep confirmed personal circumstances distinct from reported general perceptions.

For either command, age is not an intake prerequisite. Reuse a supplied dated age or birth date; otherwise ask only under skills/sponsorship-threshold-rules.md when an opened official rule shows a material age-dependent eligibility or salary-category difference. Explain the affected country/rule and ask only for the needed age or band: "Will you be [official age condition] at [relevant event]?" Fill the condition and event from that rule; do not request a full birth date when an age or band suffices. Only the parent asks; respect refusal and continue with the affected check unresolved. Do not ask again after declined disclosure unless the user reopens it.

Salary Calculator still researches the reference sponsored route for every country. If an age or status fact remains unknown, keep the affected visa check conditional under skills/sponsorship-threshold-rules.md; do not block salary research or treat the unknown as a confirmed restriction. Reuse existing dated age or birth-date answers and preserve "none known" and declined disclosure without reopening intake.

## Save and reuse

Save established facts and supplied answers to situational-profile.md in the selected run, retaining their source/date context. A new file may include facts already confirmed in profile.md without another confirmation of unchanged facts. Optional pay or age details left unspecified do not block either command's research; record "not specified" or unknown, never a zero floor, invented age or implied disclosure refusal. Date any supplied current age. Reuse existing files without adding required fields; ask later only for a material unresolved fact or report the check as unverified.

Distinguish explicit none from unknown; a legacy "not applicable" answer is not proof of no rights anywhere. Apply the shared runtime's candidate-clarification rule for dated user-approved profile notes or disclosed run-only facts, including research briefs and audits. Do not silently edit existing answers.
