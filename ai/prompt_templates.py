ANALYSIS_PROMPT = """
Analyze the following meeting summary and extract key information:

Meeting Title: {title}
Date: {date}
Discussion Summary: {summary}
Key Decisions: {decisions}
Action Items: {actions}
Participant Observations: {observations}

Extract the following:
1. FACTS: Important factual information mentioned
2. CONCERNS: Any concerns or risks discussed
3. GOALS: Goals or objectives mentioned
4. COMMITMENTS: Commitments made by participants
5. PREFERENCES: Preferences expressed
6. DECISIONS: Key decisions made

Format each as a clear, concise bullet point.
"""

PREPARATION_PROMPT = """
Generate a meeting preparation report based on the following context:

Participant: {participant_name}
Relationship Health Score: {health_score}
Previous Meetings: {meeting_count} meetings
Key Memories: {memories}
Open Commitments: {commitments}

Generate:
1. Relationship Summary
2. Key Memories to Review
3. Open Commitments
4. Important Concerns
5. Suggested Questions to Ask
6. Suggested Discussion Topics
7. Risks to Address
"""

CHAT_PROMPT = """
You are MemoMeet AI, an assistant that helps users recall information about their meetings and participants.

Context from database:
{context}

User Question: {question}

Answer based on the context provided. If the answer is not in the context, say you don't have that information.
"""

RECOMMENDATION_PROMPT = """
Based on the following relationship data, generate smart recommendations:

Participant: {participant_name}
Meetings Count: {meeting_count}
Task Completion Rate: {task_completion_rate}%
Engagement Level: {engagement_level}
Days Since Last Meeting: {days_since_last_meeting}

Generate actionable recommendations for the user.
"""
