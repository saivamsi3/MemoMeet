# MemoMeet TODO List

Checklist generated from `plan.md`.

## Phase 1: Project Foundation & Authentication
- [x] Create Flask project structure
- [x] Configure virtual environment
- [x] Install dependencies
- [x] Configure SQLite database
- [x] Create configuration files
- [x] Configure environment variables
- [x] Create Users table
- [x] Create Participants table
- [x] Create Meetings table
- [x] Implement registration
- [x] Implement login
- [x] Implement logout
- [x] Add password hashing
- [x] Add session management
- [x] Add protected routes
- [x] Create base template
- [x] Create navbar
- [x] Create sidebar
- [x] Create footer
- [x] Create responsive layout
- [x] Add dark/light theme toggle
- [x] Deliver: registration works
- [x] Deliver: login works
- [x] Deliver: dashboard access works
- [x] Deliver: database connectivity works

## Phase 2: Participant Management System
- [x] Add participant
- [x] Edit participant
- [x] Delete participant
- [x] View participant
- [x] Search participant
- [x] Store participant name
- [x] Store participant email
- [x] Store participant organization
- [x] Store participant role
- [x] Store participant interests
- [x] Store participant goals
- [x] Store participant preferences
- [x] Store participant notes
- [x] Create participants list page
- [x] Create participant profile page
- [x] Create add participant form
- [x] Create edit participant form
- [x] Deliver: participant management module

## Phase 3: Meeting Management System
- [x] Create meeting
- [x] Edit meeting
- [x] Delete meeting
- [x] View meeting
- [x] Add meeting title field
- [x] Add meeting date field
- [x] Add meeting participants field
- [x] Add discussion summary field
- [x] Add key decisions field
- [x] Add action items field
- [x] Add participant observations field
- [x] Show past meetings
- [x] Show meeting details
- [x] Show linked participants
- [x] Deliver: meeting management module

## Phase 4: Gemini AI Integration
- [x] Configure GEMINI_API_KEY env var support
- [x] Create Gemini service layer (`ai/gemini_service.py`)
- [x] Create prompt templates (`ai/prompt_templates.py`)
- [x] Send meeting summaries to Gemini (via `ai/memory_engine.py`)
- [x] Extract facts
- [x] Extract concerns
- [x] Extract goals
- [x] Extract commitments
- [x] Extract preferences
- [x] Extract decisions
- [x] Save extracted insights to database (via `ai/memory_engine.py` -> `models/memory.py`)
- [x] Deliver: AI meeting analysis (analyze endpoint added)

## Phase 5: Memory Engine
- [x] Implement fact memory
- [x] Implement preference memory
- [x] Implement goal memory
- [x] Implement concern memory
- [x] Implement commitment memory
- [x] Implement decision memory
- [x] Store memory content
- [x] Link memory to participant
- [x] Link memory to meeting source
- [x] Store importance score
- [x] Store timestamp
- [x] Create memory dashboard
- [x] Create memory detail page
- [x] Create memory filters
- [x] Deliver: long-term memory system

## Phase 6: Action Item Tracking
- [x] Store task
- [x] Store owner
- [x] Store deadline
- [x] Store status
- [x] Support status: Pending
- [x] Support status: In Progress
- [x] Support status: Completed
- [x] Support status: Overdue
- [x] Show pending tasks on dashboard
- [x] Show upcoming deadlines on dashboard
- [x] Show completed tasks on dashboard
- [x] Deliver: commitment tracking

## Phase 7: Relationship Intelligence Engine
- [x] Calculate number of meetings
- [x] Calculate engagement level
- [x] Calculate meeting frequency
- [x] Calculate task completion rate
- [x] Generate relationship health score
- [x] Show active relationships
- [x] Show at-risk relationships
- [x] Show strong relationships
- [x] Deliver: relationship analytics (backend + UI implemented)

Note: Relationship metrics are updated on meeting/action-item create/edit/delete. Remaining work: add dedicated tests and update docs/changelog.

## Phase 8: AI Meeting Preparation Engine
- [x] Load participant profile before meeting
- [x] Load previous meetings before meeting
- [x] Load memories before meeting
- [x] Load commitments before meeting
- [x] Load relationship data before meeting
- [x] Generate relationship summary
- [x] Generate key memories
- [x] Generate open commitments
- [x] Generate important concerns
- [x] Generate suggested questions
- [x] Generate suggested discussion topics
- [x] Generate risks to address
- [x] Generate PDF report
- [x] Generate printable report
- [x] Deliver: one-click preparation report
- [x] Add preparation options form (select participants, sections to include)
- [x] Add "Prepare" button to meeting details (launches preparation form)


## Phase 9: MemoMeet AI Chat
- [x] Create chat interface
- [x] Support memory retrieval questions
- [x] Search memories from user query
- [x] Load context for AI response
- [x] Run Gemini analysis for answers
- [x] Return answer in chat UI
- [x] Deliver: memory-powered AI assistant

Note: Chat UI is available at `/chat`. Backend uses `ai/memory_chat_engine.py` to build context from recent memories, meetings, and action items and calls `GeminiService` when configured. Remaining work: add streaming responses and richer context filtering.

## Phase 10: Analytics Dashboard
- [ ] Create meetings per month chart
- [ ] Create relationship score trends chart
- [ ] Create action item completion rate chart
- [ ] Create participant engagement chart
- [ ] Show total participants widget
- [ ] Show total meetings widget
- [ ] Show total memories widget
- [ ] Show pending commitments widget
- [ ] Show upcoming meetings widget
- [ ] Deliver: interactive analytics dashboard

## Phase 11: Advanced Features
- [ ] Build relationship timeline
- [ ] Add AI recommendations
- [ ] Add memory importance scoring
- [ ] Classify memory: High Priority
- [ ] Classify memory: Medium Priority
- [ ] Classify memory: Low Priority
- [ ] Add smart alerts for missed follow-ups
- [ ] Add smart alerts for overdue commitments
- [ ] Add smart alerts for declining engagement
- [ ] Deliver: advanced intelligence layer
