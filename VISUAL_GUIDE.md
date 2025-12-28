# 📸 Visual Guide - TickTick-Style Todo App

## 🖥️ Application Layout

```
┌───────────────────────────────────────────────────────────────────────────┐
│  NAVBAR: ✓ TickTick Todo                    🌓 Toggle Theme              │
├──────────┬───────────┬─────────────────────────┬──────────────────────────┤
│          │           │                         │                          │
│ SIDEBAR  │ AI CHAT   │   TASK LIST             │   DETAIL PANE            │
│ 250px    │ 350px     │   (flexible)            │   350px                  │
│          │           │                         │                          │
│ SMART    │ ┌───────┐ │ ⚠️ OVERDUE              │ ┌──────────────────────┐ │
│ VIEWS    │ │ 🤖 AI │ │ ┌─────────────────────┐ │ │ Selected Task        │ │
│          │ │Assist │ │ │☐ Pay bills          │ │ │ Details              │ │
│ 📥 Inbox │ │ Clear │ │ │  🔴 high            │ │ │                      │ │
│    (3)   │ └───────┘ │ │  📁 Budget          │ │ │ Title: Pay bills     │ │
│          │           │ │  Dec 26             │ │ │ Status: pending      │ │
│ 📅 Today │ [User]:   │ └─────────────────────┘ │ │ Priority: 🔴 high    │ │
│    (5)   │ add buy   │                         │ │ Category: Budget     │ │
│          │ milk      │ 📅 TODAY                │ │ Due: Dec 26          │ │
│ 📆 Next  │           │ ┌─────────────────────┐ │ │                      │ │
│   7 Days │ [AI]:     │ │☐ Finish report      │ │ │ DESCRIPTION:         │ │
│    (8)   │ Task 'buy │ │  🟡 medium          │ │ │ Monthly budget       │ │
│          │ milk' has │ │  📁 Work            │ │ │ review and payment   │ │
│ ─────    │ been      │ │  5:00 PM            │ │ │                      │ │
│          │ added!    │ └─────────────────────┘ │ │ CHECKLIST:           │ │
│ CATEGOR  │           │                         │ │ ☐ Review expenses    │ │
│ IES      │ [User]:   │ 📆 TOMORROW             │ │ ☐ Make payment       │ │
│          │ create    │ ┌─────────────────────┐ │ │ ☐ Update budget      │ │
│ 🔵 Work  │ task in   │ │☐ Buy groceries      │ │ │                      │ │
│    (4)   │ Shopping  │ │  📁 Shopping        │ │ │ TAGS:                │ │
│          │           │ │  #food #weekly      │ │ │ #urgent #bills       │ │
│ 🟢 Perso │ [AI]:     │ └─────────────────────┘ │ └──────────────────────┘ │
│ nal (2)  │ Created   │                         │                          │
│          │ task in   │ 📋 LATER                │                          │
│ 🟠 Shopp │ Shopping! │ ┌─────────────────────┐ │                          │
│ ing (1)  │           │ │☐ Plan vacation      │ │                          │
│          │ ┌───────┐ │ │  🔵 low             │ │                          │
│ 🟣 Univ  │ │ [____]│ │ │  📁 Personal        │ │                          │
│ ersity   │ │ Send  │ │ └─────────────────────┘ │                          │
│    (3)   │ └───────┘ │                         │                          │
│          │           │                         │                          │
└──────────┴───────────┴─────────────────────────┴──────────────────────────┘
```

---

## 🎨 Theme Comparison

### Light Mode
```
┌─────────────────────────────────┐
│ Background: White (#ffffff)     │
│ Text: Dark Gray (#2c3e50)       │
│ Sidebar: Light Gray (#f9fafb)   │
│ Borders: Light (#e0e4e8)        │
│ Hover: Subtle (#f0f2f5)         │
└─────────────────────────────────┘
```

### Dark Mode (TickTick-Inspired)
```
┌─────────────────────────────────┐
│ Background: Dark (#1e1e1e)      │
│ Text: Light Gray (#e4e4e7)      │
│ Sidebar: Darker (#202020)       │
│ Borders: Dark Gray (#3f3f46)    │
│ Hover: Medium Dark (#2d2d2d)    │
└─────────────────────────────────┘
```

---

## 🎯 Task Card Anatomy

```
┌────────────────────────────────────────────┐
│ ☐  Finish the quarterly report            │ ← Title
│    ───────────────────────────             │
│    🔴 high  📁 Work  Dec 29 5:00 PM       │ ← Badges
│    #urgent  #deadline                      │ ← Tags
└────────────────────────────────────────────┘
 ↑           ↑        ↑         ↑
Checkbox   Priority  Category  Due Date/Time
```

### Priority Colors:
- 🔴 **High**: Red (#ef4444)
- 🟡 **Medium**: Orange (#f59e0b)
- 🔵 **Low**: Blue (#3b82f6)
- ⚪ **None**: Muted gray

---

## 📱 Interaction Flow

### Creating a Task via AI

```
┌─────────────────────────────────────────────────────┐
│ STEP 1: Type in Chat                                │
│ ┌─────────────────────────────────────────────────┐ │
│ │ "create high priority task to prepare          │ │
│ │  presentation in Work due tomorrow at 2pm"      │ │
│ │                                        [Send]   │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ STEP 2: AI Responds                                 │
│ ┌─────────────────────────────────────────────────┐ │
│ │ "Created high priority task 'prepare           │ │
│ │  presentation' in Work category, due            │ │
│ │  tomorrow at 2:00 PM!"                          │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ STEP 3: Task Appears in List                        │
│ ┌─────────────────────────────────────────────────┐ │
│ │ ☐  Prepare presentation                         │ │
│ │    🔴 high  📁 Work  Tomorrow 2:00 PM          │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────┐
│ STEP 4: Click to View Details                       │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Title: Prepare presentation                     │ │
│ │ Status: pending                                 │ │
│ │ Priority: 🔴 high                               │ │
│ │ Category: Work                                  │ │
│ │ Due: 2025-12-29 at 2:00 PM                     │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🗂️ Smart Views Explained

### 📥 Inbox
Shows tasks that:
- Have no category assigned, OR
- Are in the "Inbox" category

```
Example:
☐ Buy milk (no category)
☐ Random idea (Inbox)
```

### 📅 Today
Shows tasks where:
- due_date_only = today's date

```
Example (if today is Dec 28):
☐ Finish report (due: Dec 28)
☐ Call client (due: Dec 28 at 3pm)
```

### 📆 Next 7 Days
Shows tasks where:
- due_date_only is between today and 7 days from now

```
Example (if today is Dec 28):
☐ Team meeting (due: Dec 30)
☐ Submit proposal (due: Jan 2)
```

### Category Filter (e.g., Work)
Shows tasks where:
- category = selected category
- status = pending

```
Example (Work category):
☐ Finish report
☐ Prepare presentation
☐ Review code
```

---

## 📋 Task Sections Logic

Tasks are automatically grouped by due date:

```
if due_date_only < today:
    → ⚠️ OVERDUE

elif due_date_only == today:
    → 📅 TODAY

elif due_date_only == tomorrow:
    → 📆 TOMORROW

else:
    → 📋 LATER (includes tasks with no due date)
```

---

## 🎭 Detail Pane Components

### When NO Task Selected:
```
┌────────────────────────┐
│                        │
│        📝              │
│                        │
│  Select a task to      │
│  view details          │
│                        │
└────────────────────────┘
```

### When Task Selected:
```
┌────────────────────────────────┐
│ TITLE                          │
│ Prepare presentation           │
│                                │
│ ───────────────────────────    │
│                                │
│ DETAILS                        │
│ Status: pending                │
│ Priority: 🔴 high              │
│ Category: Work                 │
│ Due: Dec 29 at 2:00 PM        │
│                                │
│ ───────────────────────────    │
│                                │
│ DESCRIPTION                    │
│ Quarterly review slides for    │
│ the team meeting               │
│                                │
│ ───────────────────────────    │
│                                │
│ CHECKLIST                      │
│ ☐ Research data                │
│ ☐ Create slides                │
│ ☑ Practice delivery            │
│                                │
│ ───────────────────────────    │
│                                │
│ TAGS                           │
│ #urgent #presentation          │
│                                │
└────────────────────────────────┘
```

---

## 🎨 Default Category Colors

```
🔵 Inbox      #3b82f6  (Blue)
🔴 Work       #ef4444  (Red)
🟢 Personal   #10b981  (Green)
🟠 Shopping   #f59e0b  (Orange)
🟣 University #8b5cf6  (Purple)
🔵 Budget     #06b6d4  (Cyan)
🔴 Health     #ec4899  (Pink)
🟢 Projects   #14b8a6  (Teal)
```

---

## ⌨️ Keyboard Shortcuts

Currently available:
- **Enter** in chat input: Send message
- **Click** task: Select and view details
- **Click** checkbox: Toggle completion
- **Click** sidebar item: Filter tasks

*Future enhancement: Add more keyboard shortcuts*

---

## 🎯 Task Status Indicators

### Visual States:

**Pending Task:**
```
☐  Buy groceries
   📁 Shopping  Tomorrow
```

**Completed Task:**
```
☑  Buy milk
   ────────────
   (strikethrough, muted color)
```

**Overdue Task:**
```
☐  Pay bills
   🔴 high  📁 Budget  Dec 26
   (shown in Overdue section)
```

**Selected Task:**
```
┌─────────────────────────────┐  ← Blue border
│ ☐  Finish report            │
│    🟡 medium  📁 Work       │
└─────────────────────────────┘
```

---

## 🔄 Auto-Refresh Behavior

The UI automatically refreshes in these scenarios:

1. **After AI Command:**
   ```
   User sends message → AI processes → Tasks reload → Categories reload
   ```

2. **After Checkbox Toggle:**
   ```
   Click checkbox → Status updates → Tasks reload
   ```

3. **After Task Selection:**
   ```
   Click task → Detail pane updates (no full reload)
   ```

---

## 🎨 CSS Classes Reference

### Task Priority Classes
- `.priority-high` → Red background
- `.priority-medium` → Orange background
- `.priority-low` → Blue background

### Task State Classes
- `.task-title.completed` → Strikethrough, muted
- `.task-item.selected` → Blue border
- `.task-item:hover` → Shadow, slight lift

### Theme Classes
- `[data-theme="light"]` → Light mode
- `[data-theme="dark"]` → Dark mode

---

## 📊 Count Badges

Sidebar counts update in real-time:

```
📥 Inbox    (3)  ← 3 pending tasks in Inbox
📅 Today    (5)  ← 5 tasks due today
📆 Next     (8)  ← 8 tasks due in next 7 days
   7 Days

🔵 Work     (4)  ← 4 pending tasks in Work
🟢 Personal (2)  ← 2 pending tasks in Personal
```

**Only counts pending tasks** (not completed)

---

## 🎉 Interactive Elements

### Clickable Elements:
1. **Sidebar Items**: Filter tasks
2. **Task Cards**: Select for detail view
3. **Checkboxes**: Toggle completion
4. **Theme Toggle**: Switch theme
5. **Clear Chat Button**: Clear chat history
6. **Send Button**: Send AI message

### Hover Effects:
- Task cards lift slightly
- Sidebar items highlight
- Buttons change opacity
- Checkboxes show focus

---

## 🚀 Example User Journey

### New User Flow:

1. **Open App** → See welcome empty state
2. **Type in Chat**: "add buy milk"
3. **See Task Appear** in Inbox
4. **Click Task** → View details in right pane
5. **Try Theme Toggle** → Switch to dark mode
6. **Create Complex Task**: "create high priority task to study in University due tomorrow with steps: chapter 1, practice problems"
7. **See Task Organized** in Tomorrow section
8. **Click Checkbox** → Mark first task complete
9. **Explore Categories** → Click Work category
10. **Filter by Date** → Click Today view

---

## 📐 Layout Dimensions

```
Total Width: 100vw (viewport width)
Total Height: 100vh (viewport height)

Columns:
- Sidebar:    250px (fixed)
- AI Chat:    350px (fixed)
- Task List:  1fr   (flexible, takes remaining space)
- Detail:     350px (fixed)

Rows:
- Navbar:     50px (fixed)
- Content:    1fr  (flexible, fills remaining height)
```

### Responsive Behavior:
*Current: Fixed layout for desktop*
*Future: Add mobile responsive breakpoints*

---

## 🎨 Empty States

### Empty Task List:
```
┌─────────────────────────┐
│                         │
│         ✨              │
│                         │
│   No tasks here.        │
│   Ask AI to create      │
│   some!                 │
│                         │
└─────────────────────────┘
```

### No Task Selected:
```
┌─────────────────────────┐
│                         │
│         📝              │
│                         │
│   Select a task to      │
│   view details          │
│                         │
└─────────────────────────┘
```

---

This visual guide should help you understand and navigate the TickTick-style Todo App interface! 🎉
