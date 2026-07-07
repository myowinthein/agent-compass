Using the candidate profile, situational profile, and answers from Step 1, discover a candidate country shortlist for each track. Do not brainstorm countries from memory or general reputation. Every country included must be traceable to a real, checkable source.

Part A — Direct filtering (no research needed, apply immediately)

1. Remove any country listed under Exclusions in Step 1, from both tracks.
2. For the Remote track only: calculate the UTC time difference between each remaining country and my current location. Remove any country outside the maximum hours I specified in Step 1. Do not apply this filter to the Sponsorship track, since relocation removes the timezone constraint.

Show the result of this filtering step as two lists before continuing: "Remote candidate universe" and "Sponsorship candidate universe."

Part B — Generate research prompts for the remaining candidates

Generate two separate ready-to-copy research prompts, one per track. Each must instruct the researcher to use current web research (prioritizing sources from the last 12 months), not memory or general reputation.

Remote Discovery Research Prompt should ask the researcher to identify, from the Remote candidate universe, countries where:

- remote hiring for this candidate's role and skillset is a common, well-established practice, not a rare exception
- typical remote salary for this role realistically meets or exceeds the minimum monthly salary from Step 1
- evidence comes from remote job boards, remote hiring reports, salary surveys, or company remote-hiring policies

Sponsorship Discovery Research Prompt should ask the researcher to identify, from the Sponsorship candidate universe, countries where:

- a real, named, documented work-visa sponsorship pathway exists for this candidate's role and skillset
- the candidate's occupation appears on any official shortage-occupation or in-demand skills list, if one exists
- citizenship-specific visa reciprocity, restrictions, or friction are considered, based on the situational profile
- evidence comes from official government immigration sources, visa program pages, or recruiter sponsorship guides

For both prompts, require this exact output format per country:

Country: [name]
Reason for inclusion: [evidence-based reasoning]
Source: [name of source]
Date: [date of source]

Important rule for both prompts:

Do not include a country based on reputation alone. If a country is commonly assumed to be a good fit but no real, dated source supports it, leave it out and do not mention it. Only include countries with actual supporting evidence.

Output:

- Two ready-to-copy research prompts, clearly labeled "Remote Discovery Research Prompt" and "Sponsorship Discovery Research Prompt"
- Do not attempt to answer the research questions yourself in this step

After generating these two prompts, run each one as a separate, isolated research task. If you are able to run these as isolated sub-agent tasks, do so with the following strict briefs:

- Agent 1 receives only the Remote Discovery Research Prompt. Its only job is to run that research and save the results to remote-candidates.md. It must not produce, draft, or save anything related to the Sponsorship track.
- Agent 2 receives only the Sponsorship Discovery Research Prompt. Its only job is to run that research and save the results to sponsorship-candidates.md. It must not produce, draft, or save anything related to the Remote track.

Each agent works from its own prompt only, with no access to your prior reasoning in this conversation. If you cannot guarantee that isolation, show me the two prompts and wait for me to bring back the results myself before continuing.

Do not proceed to Step 3 until both remote-candidates.md and sponsorship-candidates.md exist in the workspace.
