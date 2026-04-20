import json

with open("research/content_quality_audit.json") as f:
    data = json.load(f)

for d in data:
    print(f"\n{'='*50}")
    print(f"Expert: {d['expert']}")
    print(f"Verdict: {d['VALIDATION_VERDICT']}")
    print(f"Topic Relevance: {d['TOPIC_RELEVANCE_SCORE']}/10")
    print(f"TR Evidence: {d['TOPIC_RELEVANCE_EVIDENCE']}")
    print(f"Original Research: {d['ORIGINAL_RESEARCH']}")
    print(f"Depth Score: {d['DEPTH_SCORE']}/10")
    print(f"Unique Angle: {d['UNIQUE_ANGLE']}")
    print(f"Playbook Value: {d['PLAYBOOK_VALUE']}/10")
    print(f"Reasoning: {d['VERDICT_REASONING']}")