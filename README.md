# Event-scheduler-using-Python-scripting

**Run script using**  ``` ./run_script.sh```  
**Run unit test**  ```pytest ```   


**Project Overview:**

``
Develop a command-line tool that allows users to schedule, categorize, and analyze their daily events. The tool will focus on efficient event management, conflict detection, and generating insightful reports.
``


**Key Features**

***1. Event Management***
```
Create Events: Users can add new events with details including name, category, start time, and duration.
Update Events: Modify existing events, including changing the start time or duration.
Delete Events: Remove events from the schedule.
Event Storage: Events are stored using a dictionary with tuples for details, keyed by the start time of the event.

```

***2. Conflict Detection***
```
Overlap Detection: The tool checks for overlapping events within the same date.
Conflict Resolution: Provides suggestions to resolve conflicts, such as adjusting start times or durations.
```
***3. Event Categorization***
```
Category Assignment: Users can assign categories (e.g., Work, Exercise, Leisure) to events.
Category Filtering: Filter and view events based on their assigned categories.
```
***5. Event Analytics***
```
Reports Generation: Generate reports on:
Total time spent per category.
Busiest days with the most events.
Trends over time, showing category-wise duration for each day.
Efficient Data Handling: Uses generators to iterate through events and produce reports.
```
***7. Command-Line Interface (CLI)***
```
User-Friendly CLI: Supports various commands for interacting with the scheduler, including:
Adding events: -add
Viewing schedules: -list
Filtering by category: -filter
Generating reports: -report
Updating events: -update
Deleting events: -delete

```
**Usage**


***Adding an Event***
```
./run_script.sh -add -name "My Birthday " -category "Personal" -start "2024-04-14 09:00" -duration 60
```
***Viewing Events***
```
./run_script.sh -list

```

***Filtering by Category***
```
./run_script.sh -filter -category "Personal"

```
***Generating a Report***
```
./run_script.sh -report
```

***Updating an Event***
```
./run_script.sh -update -keys "2024-4-14 09:00" -duration +30
./run_script.sh -update -keys "2024-09-10 09:00" "2024-04-14 09:00" -duration  -10  -category "Education"
```

***Deleting an Event***
```
./run_script.sh  -delete -start "2024-04-14 09:00"

```
