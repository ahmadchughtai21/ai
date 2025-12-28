# ✅ Testing Checklist - TickTick-Style Todo App

## 🎯 Complete Testing Guide

Use this checklist to verify all features are working correctly.

---

## 🚀 Pre-Testing Setup

- [ ] Virtual environment activated
- [ ] Django server running at http://localhost:8000
- [ ] Groq API key configured in .env
- [ ] Migrations applied successfully
- [ ] Default categories created (8 categories)
- [ ] Browser: Chrome, Firefox, or Safari
- [ ] Browser console open (F12) to check for errors

---

## 1️⃣ Database & Backend Testing

### Models
- [ ] Category model created with name and color fields
- [ ] SubTask model created with task FK and order
- [ ] Task model extended with new fields (category, priority, due_date_only, due_time)
- [ ] All new fields are nullable or have defaults
- [ ] Tag model exists and works

### Migrations
```bash
# Run these commands to verify:
python manage.py showmigrations
# Should show todo_app.0002 is applied

python manage.py check
# Should show: System check identified no issues
```

- [ ] Migration 0002 applied successfully
- [ ] No migration warnings or errors
- [ ] Database schema updated correctly

### Admin Panel
Visit http://localhost:8000/admin

- [ ] Login with superuser credentials
- [ ] See Category in admin (with task count)
- [ ] See Task in admin (with inline subtasks)
- [ ] See SubTask in admin
- [ ] See Tag in admin
- [ ] See ChatMessage in admin
- [ ] Can create/edit categories with color picker
- [ ] Can add subtasks inline when creating tasks
- [ ] Filters work (status, priority, category)

---

## 2️⃣ API Testing

### Using Browser API View
Visit http://localhost:8000/api/

#### Categories API
- [ ] GET /api/categories/ returns list with 8 default categories
- [ ] Each category has: id, name, color, task_count, created_at
- [ ] POST new category with {"name": "Testing", "color": "#ff0000"}
- [ ] GET /api/categories/{id}/ retrieves specific category
- [ ] PATCH /api/categories/{id}/ updates category name or color
- [ ] DELETE /api/categories/{id}/ deletes category

#### Tasks API
- [ ] GET /api/tasks/ returns list of tasks
- [ ] Response includes: category_name, category_detail, priority, subtasks
- [ ] POST new task with all fields:
```json
{
  "title": "Test Task",
  "description": "Testing TickTick features",
  "category_id": 1,
  "priority": "high",
  "due_date_only": "2025-12-30",
  "due_time": "14:00:00",
  "tag_ids": []
}
```
- [ ] PATCH /api/tasks/{id}/ updates task fields
- [ ] POST /api/tasks/{id}/add_subtask/ adds subtask
- [ ] DELETE /api/tasks/{id}/ deletes task

#### SubTasks API
- [ ] GET /api/subtasks/ lists all subtasks
- [ ] PATCH /api/subtasks/{id}/ toggles is_completed
- [ ] DELETE /api/subtasks/{id}/ deletes subtask

#### Chat API
- [ ] POST /api/chat/ with {"message": "add test task"} works
- [ ] Response contains {"response": "..."}
- [ ] GET /api/chat/history/ shows message history
- [ ] POST /api/chat/clear/ clears history

---

## 3️⃣ AI Integration Testing

### Basic Commands

**Simple Task Creation:**
- [ ] "add buy milk" → Creates task in Inbox
- [ ] "add test task" → Creates task successfully
- [ ] Task appears in task list immediately

**Task with Category:**
- [ ] "create task in Work category" → Assigns to Work
- [ ] "add task to Shopping" → Uses existing Shopping category
- [ ] "create task in NewCategory" → Auto-creates NewCategory

**Task with Priority:**
- [ ] "add high priority task" → Sets priority to high
- [ ] "create important task" → Sets priority to high (synonym)
- [ ] "add low priority task" → Sets priority to low
- [ ] "create normal task" → Sets priority to medium

**Task with Due Date:**
- [ ] "add task due today" → Sets today's date
- [ ] "add task due tomorrow" → Sets tomorrow's date
- [ ] "create task due next monday" → Calculates correct date
- [ ] "add task due 2025-12-31" → Sets explicit date

**Task with Due Time:**
- [ ] "add task due at 3pm" → Sets time to 3:00 PM
- [ ] "create task at 9:30 AM" → Sets time to 9:30 AM
- [ ] "add task tomorrow at 5pm" → Sets date AND time

**Task with Subtasks:**
- [ ] "add groceries with milk, bread, eggs" → Creates 3 subtasks
- [ ] "create task with steps: step1, step2" → Creates subtasks
- [ ] Subtasks appear in correct order

**Complex Task:**
- [ ] "create high priority task to prepare presentation in Work category due tomorrow at 2pm with steps: research, create slides, practice"
- [ ] Verify all fields set correctly
- [ ] Check task appears in Tomorrow section
- [ ] Verify subtasks created

### Update Commands

**Mark Complete:**
- [ ] "mark buy milk as done" → Status changes to completed
- [ ] "complete buy milk" → Same result
- [ ] Task moves out of pending list

**Update Priority:**
- [ ] "set buy milk priority to high" → Priority updates
- [ ] "change buy milk to low priority" → Priority updates

**Update Category:**
- [ ] "move buy milk to Shopping" → Category changes
- [ ] Auto-creates category if needed

**Update Due Date:**
- [ ] "change buy milk due to next friday" → Due date updates

### Query Commands

**List Tasks:**
- [ ] "show my tasks" → Lists all pending tasks
- [ ] "what tasks do I have?" → Same result
- [ ] Response is natural language, not JSON

**Count Tasks:**
- [ ] "how many tasks?" → Returns count

**Filter by Category:**
- [ ] "show Work tasks" → Filters by category

### Delete Commands

**Delete Single:**
- [ ] "delete buy milk" → Removes task
- [ ] Task disappears from list

**Delete All:**
- [ ] "delete all tasks" → Removes all tasks
- [ ] Inbox count becomes 0

### Scope Restriction

**Non-Task Queries (Should Reject):**
- [ ] "how to make biryani?" → Rejects with message
- [ ] "what's the weather?" → Rejects
- [ ] "help me code" → Rejects
- [ ] "tell me a joke" → Rejects
- [ ] Response: "Sorry, I can't help with that. I'm a todo list assistant..."

### Edge Cases

**Invalid Task Name:**
- [ ] "mark nonexistent task as done" → Error message in terminal
- [ ] User sees friendly "task not found" message

**Empty Input:**
- [ ] Send empty message → Nothing happens or error

**Very Long Task Title:**
- [ ] Create task with 200+ character title → Handles gracefully

---

## 4️⃣ User Interface Testing

### Layout & Structure

**Page Load:**
- [ ] Page loads without errors
- [ ] 4-pane layout visible
- [ ] No JavaScript console errors
- [ ] No broken images or missing resources

**Navbar:**
- [ ] "✓ TickTick Todo" title visible
- [ ] Theme toggle button present
- [ ] Navbar spans full width

**Sidebar (250px):**
- [ ] Smart Views section visible
- [ ] Inbox, Today, Next 7 Days items present
- [ ] Categories section visible
- [ ] All 8 default categories listed
- [ ] Category colors showing correctly
- [ ] Task counts showing

**AI Chat Pane (350px):**
- [ ] Header shows "🤖 AI Assistant"
- [ ] Clear button present
- [ ] Messages area scrollable
- [ ] Input field present
- [ ] Send button present

**Task List Pane (flexible):**
- [ ] Shows empty state when no tasks
- [ ] Sections appear when tasks exist
- [ ] Tasks render correctly
- [ ] Scrollable content

**Detail Pane (350px):**
- [ ] Shows empty state initially
- [ ] Updates when task selected
- [ ] All task fields visible

### Theme Toggle

**Light Mode:**
- [ ] Click theme toggle
- [ ] Background turns white
- [ ] Text turns dark
- [ ] Sidebar is light gray
- [ ] Borders are subtle
- [ ] All text readable

**Dark Mode:**
- [ ] Click theme toggle again
- [ ] Background turns dark (#1e1e1e)
- [ ] Text turns light
- [ ] Sidebar is darker (#202020)
- [ ] TickTick-style dark palette
- [ ] All text readable

**Persistence:**
- [ ] Set to dark mode
- [ ] Refresh page
- [ ] Still in dark mode (localStorage)
- [ ] Switch to light
- [ ] Refresh again
- [ ] Still in light mode

### Chat Functionality

**Sending Messages:**
- [ ] Type message in input
- [ ] Click Send → Message appears
- [ ] Press Enter → Message appears
- [ ] Input clears after sending
- [ ] User message aligned right (blue)
- [ ] AI message aligned left (gray)

**Chat History:**
- [ ] Send multiple messages
- [ ] Scroll to see older messages
- [ ] Messages persist on page refresh
- [ ] Click Clear → Confirms
- [ ] Click OK → All messages cleared

**Message Formatting:**
- [ ] Bold text with **text** renders
- [ ] Line breaks with \n work
- [ ] Long messages wrap correctly

### Sidebar Interaction

**Smart Views:**
- [ ] Click Inbox → Filters to Inbox tasks
- [ ] Active state highlights (blue border)
- [ ] Click Today → Filters to today's tasks
- [ ] Click Next 7 Days → Filters correctly

**Categories:**
- [ ] Click Work → Filters to Work tasks
- [ ] Category becomes active
- [ ] Task list updates
- [ ] Count badge accurate

**Hover Effects:**
- [ ] Hover over sidebar items → Background changes
- [ ] Cursor changes to pointer
- [ ] Smooth transition

### Task List Display

**Task Sections:**
- [ ] Overdue section appears when tasks past due
- [ ] Today section shows today's tasks
- [ ] Tomorrow section shows tomorrow's tasks
- [ ] Later section shows future/no-date tasks

**Task Cards:**
- [ ] Checkbox on left
- [ ] Task title displays
- [ ] Priority badge shows (colored)
- [ ] Category icon and name display
- [ ] Due date shows formatted ("Today", "Tomorrow", "Dec 30")
- [ ] Due time shows if set
- [ ] Tags display as chips

**Task Interaction:**
- [ ] Hover over task → Card lifts slightly
- [ ] Hover → Shadow appears
- [ ] Click task → Selects (blue border)
- [ ] Detail pane updates

**Checkbox:**
- [ ] Click checkbox → Task marked complete
- [ ] Title gets strikethrough
- [ ] Color becomes muted
- [ ] Task list refreshes
- [ ] Completed task removed from view

**Empty State:**
- [ ] When no tasks in filter → Shows "No tasks here" message
- [ ] Icon displays
- [ ] Helpful text suggests using AI

### Detail Pane

**Initial State:**
- [ ] Shows "Select a task to view details"
- [ ] Empty state icon visible

**After Selection:**
- [ ] Task title displays large
- [ ] Details section shows:
  - [ ] Status
  - [ ] Priority (with color)
  - [ ] Category
  - [ ] Due date (if set)
- [ ] Description shows (if exists)
- [ ] Subtasks section shows (if exist)
  - [ ] Each subtask listed
  - [ ] Checkboxes present
  - [ ] Completed subtasks struck through
- [ ] Tags section shows (if exist)
  - [ ] Tags as chips

**Subtask Interaction:**
- [ ] Click subtask checkbox → Logs to console
- [ ] (Note: Full functionality requires backend endpoint)

### Scrolling

**All Panes Scroll Independently:**
- [ ] Sidebar scrolls (if many categories)
- [ ] Chat messages scroll
- [ ] Task list scrolls
- [ ] Detail pane scrolls
- [ ] No horizontal scrollbars
- [ ] Scrollbars match theme

**Custom Scrollbars:**
- [ ] Scrollbars styled (8px width)
- [ ] Track color matches theme
- [ ] Thumb color subtle
- [ ] Hover changes thumb color

### Responsive Behavior

**Window Resize:**
- [ ] Task list pane adjusts width (1fr)
- [ ] Other panes stay fixed width
- [ ] No layout breaks
- [ ] All content visible

**Overflow Handling:**
- [ ] Long task titles wrap correctly
- [ ] Long descriptions wrap in detail
- [ ] Tags wrap to new line
- [ ] No text cutoff

---

## 5️⃣ Task Organization Testing

### Smart Views Logic

**Inbox:**
- [ ] Create task without category → Shows in Inbox
- [ ] Create task in "Inbox" category → Shows in Inbox
- [ ] Create task in other category → Does NOT show in Inbox

**Today:**
- [ ] Create task with today's date → Shows in Today
- [ ] Create task with tomorrow's date → Does NOT show in Today
- [ ] No due date → Does NOT show in Today
- [ ] Count badge accurate

**Next 7 Days:**
- [ ] Create task due in 3 days → Shows
- [ ] Create task due in 8 days → Does NOT show
- [ ] Create task due yesterday → Does NOT show
- [ ] Count badge accurate

### Task Sections

**Overdue:**
- [ ] Task with past due date appears
- [ ] Shown at top of list
- [ ] Red/warning styling

**Today:**
- [ ] Tasks due today appear
- [ ] Shown in correct section

**Tomorrow:**
- [ ] Tasks due tomorrow appear
- [ ] Shown in correct section

**Later:**
- [ ] Future tasks appear
- [ ] Tasks without due date appear
- [ ] Shown at bottom

### Priority Display

**High Priority:**
- [ ] Red badge (#ef4444)
- [ ] Text says "high"
- [ ] Badge has red background (transparent)

**Medium Priority:**
- [ ] Orange badge (#f59e0b)
- [ ] Text says "medium"

**Low Priority:**
- [ ] Blue badge (#3b82f6)
- [ ] Text says "low"

**No Priority:**
- [ ] No badge shown

### Category Display

**Category Indicator:**
- [ ] Folder icon (📁) shows
- [ ] Category name displays
- [ ] Correct category assigned

**Category Colors:**
- [ ] Sidebar category dots match colors
- [ ] Work is red
- [ ] Personal is green
- [ ] Shopping is orange
- [ ] etc.

---

## 6️⃣ Data Persistence Testing

### After Browser Refresh

**Tasks:**
- [ ] All tasks still visible
- [ ] Categories preserved
- [ ] Priorities preserved
- [ ] Due dates preserved
- [ ] Subtasks preserved
- [ ] Tags preserved

**Chat History:**
- [ ] Messages persist
- [ ] Order maintained

**Theme:**
- [ ] Selected theme persists
- [ ] (via localStorage)

**Task Selection:**
- [ ] Selection NOT persisted (expected)

### After Server Restart

**Stop and restart Django server:**
```bash
# Stop: CTRL+C
# Start: python manage.py runserver
```

- [ ] All data still in database
- [ ] Tasks load correctly
- [ ] Categories exist
- [ ] No data loss

---

## 7️⃣ Error Handling

### Network Errors

**Simulate offline:**
- [ ] Disconnect internet
- [ ] Try to send AI message
- [ ] Error shown gracefully
- [ ] App doesn't crash

### API Errors

**Invalid Data:**
- [ ] Create task with invalid category_id
- [ ] Error logged to console
- [ ] User sees friendly message

### Groq API Errors

**Invalid API Key:**
- [ ] Change .env to invalid key
- [ ] Restart server
- [ ] Send message
- [ ] Error logged: "Error communicating with Groq"

**Rate Limit:**
- [ ] Send many messages quickly
- [ ] If rate limited, error shown
- [ ] App still functional

---

## 8️⃣ Performance Testing

### Load Time

**Initial Page Load:**
- [ ] Page loads in < 2 seconds
- [ ] No lag in rendering
- [ ] Smooth animations

**Task List Rendering:**
- [ ] 50+ tasks render quickly
- [ ] No visible lag
- [ ] Scrolling smooth

### AI Response Time

**Message Send to Response:**
- [ ] Simple command: ~1-2 seconds
- [ ] Complex command: ~2-3 seconds
- [ ] Acceptable latency

### UI Responsiveness

**Interactions:**
- [ ] Click sidebar item → Instant filter
- [ ] Click task → Instant detail update
- [ ] Hover → Instant visual feedback
- [ ] Checkbox → Quick update

---

## 9️⃣ Cross-Browser Testing

### Chrome
- [ ] All features work
- [ ] Layout correct
- [ ] No console errors

### Firefox
- [ ] All features work
- [ ] Layout correct
- [ ] Scrollbars styled

### Safari (macOS)
- [ ] All features work
- [ ] Layout correct
- [ ] Date inputs work

### Edge
- [ ] All features work
- [ ] Layout correct

---

## 🔟 Accessibility Testing

### Keyboard Navigation

- [ ] Tab through interactive elements
- [ ] Checkboxes focusable
- [ ] Buttons focusable
- [ ] Input fields focusable
- [ ] Enter key sends message

### Screen Reader

**Basic Checks:**
- [ ] Task titles read correctly
- [ ] Buttons have labels
- [ ] Form inputs labeled

### Color Contrast

**WCAG Compliance:**
- [ ] Text readable in light mode
- [ ] Text readable in dark mode
- [ ] Priority colors distinguishable
- [ ] Focus indicators visible

---

## 1️⃣1️⃣ Mobile Responsive (Future Enhancement)

*Note: Current version is desktop-focused. Mark these for future testing when mobile responsive is added.*

- [ ] Layout adapts to small screens
- [ ] Sidebar collapsible
- [ ] Touch gestures work
- [ ] No horizontal scroll

---

## 📊 Final Verification

### Feature Completeness

- [ ] ✅ Categories with colors
- [ ] ✅ Priorities (4 levels)
- [ ] ✅ Due dates (separate date/time)
- [ ] ✅ Subtasks
- [ ] ✅ Tags
- [ ] ✅ Smart views
- [ ] ✅ 4-pane layout
- [ ] ✅ Theme toggle
- [ ] ✅ AI integration
- [ ] ✅ Task sections
- [ ] ✅ Detail pane

### Documentation

- [ ] README.md updated
- [ ] UPGRADE_GUIDE.md created
- [ ] AI_PROMPT_GUIDE.md created
- [ ] VISUAL_GUIDE.md created
- [ ] IMPLEMENTATION_SUMMARY.md created
- [ ] setup_categories.py created

### Backward Compatibility

- [ ] Old tasks work without changes
- [ ] Simple AI commands work
- [ ] Can create tasks without new fields
- [ ] No breaking changes

---

## ✅ Test Results Summary

**Total Tests:** ~200+
**Passed:** ___
**Failed:** ___
**Skipped:** ___

**Critical Issues Found:** ___
**Minor Issues Found:** ___

**Overall Status:** 🟢 Ready for Use / 🟡 Needs Fixes / 🔴 Major Issues

---

## 🐛 Issues Found

*Document any issues discovered during testing:*

1. Issue: ___
   - Severity: Critical / Major / Minor
   - Steps to reproduce: ___
   - Expected: ___
   - Actual: ___

2. Issue: ___
   - etc...

---

## 🎉 Sign-off

**Tester:** _______________
**Date:** _______________
**Status:** ✅ Approved / ❌ Rejected
**Notes:** _______________

---

**Use this checklist to ensure all features work correctly before deploying to production!** 🚀
