# Database Schema

## Tables

### users
- id (PK), username, email, password_hash, theme, created_at, updated_at

### participants
- id (PK), user_id (FK), name, email, organization, role, interests, goals, preferences, notes, created_at, updated_at

### meetings
- id (PK), user_id (FK), title, date, discussion_summary, key_decisions, action_items, participant_observations, created_at, updated_at

### meeting_participants
- id (PK), meeting_id (FK), participant_id (FK), created_at

### memories
- id (PK), meeting_id (FK), participant_id (FK), user_id (FK), memory_type, content, importance_score, created_at

### action_items
- id (PK), meeting_id (FK), participant_id (FK), user_id (FK), task, owner, deadline, status, created_at, updated_at

### relationships
- id (PK), user_id (FK), participant_id (FK), meeting_count, engagement_level, meeting_frequency, task_completion_rate, health_score, created_at, updated_at

### recommendations
- id (PK), user_id (FK), participant_id (FK), recommendation_type, content, priority, is_read, created_at

### notifications
- id (PK), user_id (FK), notification_type, title, message, is_read, created_at

### analytics
- id (PK), user_id (FK), metric_name, metric_value, recorded_at
